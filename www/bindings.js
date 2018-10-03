/* global window, testability */
/* exported instrumentBrowser */
'use strict';

var instrumentBrowser = function (window) {
    window = window || this;
    var setImmediate = window.setImmediate || window.setTimeout;

    function patchFunction(set, clear, filterTime) {
        var setFn = window[set];

        if (!setFn) {
            return;
        }

        var clearFn = window[clear];
        var stack = {};
        var sets = {};

        function endWait(reference) {
            var task = sets[reference];
            if (task) {
                setImmediate(task.end);
                delete sets[reference];
            }
        }

        window[set] = function () {
            var cb = arguments[0];
            var ref;
            var time = arguments[1] || 0;

            if (!filterTime || (time < 5000 && stack[cb] !== cb)) {

                arguments[0] = function () {
                    stack[cb] = cb;
                    var rtn;
                    try {
                        rtn = cb.apply(window, arguments);
                    }
                    finally {
                        delete stack[cb];
                        endWait(ref);
                    }
                    return rtn;
                };

                ref = setFn.apply(window, arguments);
                sets[ref] = window.testability.wait.start();
            }
            else {
                ref = setFn.apply(window, arguments);
            }

            return ref;
        };
        window[clear] = function () {
            var rtn = clearFn.apply(window, arguments);
            endWait(arguments[0]);
            return rtn;
        };

        window[set].restore = function () {
            window[set] = setFn;
        };
        window[clear].restore = function () {
            window[clear] = clearFn;
        };
    }

    function patchPromiseFunction(set) {
        var setFn = window[set];

        if (!setFn) {
            return;
        }

        window[set] = function () {
            var ref;

            function keepOn(result) {
                setImmediate(window.testability.wait.oneLess);
                return result;
            }

            ref = setFn.apply(window, arguments);
            ref.then(keepOn).catch(keepOn);
            window.testability.wait.oneMore();

            return ref;
        };
        window[set].restore = function () {
            window[set] = setFn;
        };
    }

    patchFunction('setTimeout', 'clearTimeout', true);
    patchFunction('setImmediate', 'clearImmediate', false);
    patchPromiseFunction('fetch');

    var oldOpen = window.XMLHttpRequest.prototype.open;
    window.XMLHttpRequest.prototype.open = function () {
        if(window.testability) {
            var task;
            this.addEventListener('readystatechange', function () {
                if (this.readyState === 4 && task) {
                    setImmediate(task.end);
                }
                if (this.readyState === 1 && !task) {
                    task = testability.wait.start();
                }
            }, false);
            var abort = this.abort;
            this.abort = function () {
                if (task) {
                    setImmediate(task.end);
                }
                abort.apply(this, arguments);
            };
        }
        oldOpen.apply(this, arguments);
    };


    function whichEvents(){
        var t;
        var el = document.createElement('fakeelement');
        var transitions = {
            'OTransition':{
                transitionend:'oTransitionEnd', transitionstart: 'oTransitionStart',
                animationend:'oAnimationEnd', animationstart: 'oAnimationStart'
            },
            'MozTransition':{
                transitionend:'transitionend', transitionstart: 'transitionstart',
                animationend:'animationend', animationstart: 'animationstart'
            },
            'WebkitTransition':{
                transitionend:'webkitTransitionEnd', transitionstart: 'webkitTransitionStart',
                animationend:'webkitAnimationEnd', animationstart: 'webkitAnimationStart'
            },
        };

        for(t in transitions){
            if( el.style[t] !== undefined ){
                return transitions[t];
            }
        }

        return {
            transitionend:'transitionend', transitionstart: 'transitionstart',
            animationend:'animationend', animationstart: 'animationstart'
        };
    }

    var events = whichEvents();

    function startHandler(event) {
        if(event.target && !event.target._testabilityAnimating) {
            var style = window.getComputedStyle(event.target);
            var animationIterationCount =
                style['animation-iteration-count'] ||
                style['-webkit-animation-iteration-count'];
            if(animationIterationCount && animationIterationCount.indexOf('infinite') >= 0) {
                return;
            }
            event.target._testabilityAnimating = true;
            window.testability.wait.oneMore();
        }
    }

    function endHandler(event) {
        if(event.target && event.target._testabilityAnimating) {
            setImmediate(window.testability.wait.oneLess);
            delete event.target._testabilityAnimating;
        }
    }

    //TODO: Find a way to handle transitions as transitionstart is not standard
    //XXX: It seems that edge/ie10/firefox will support these but chrome do
    //not trigger transition start at all, transition end does trigger.
    document.addEventListener(events.transitionstart, startHandler);
    document.addEventListener(events.transitionend, endHandler);

    document.addEventListener(events.animationstart, startHandler);
    document.addEventListener(events.animationend, endHandler);

    var animate = Element.prototype.animate;

    if(animate) {

        Element.prototype.animate = function () {
            var animation = animate.apply(this, arguments);

            if(animation.effect && animation.effect.activeDuration !== Infinity) {
                testability.wait.for(animation.finished);
            }

            return animation;
        };
    }

    return {
        animationEvents: events,
        restore: function () {
            window.setTimeout.restore();
            window.clearTimeout.restore();
            if(window.setImmediate) {
                window.setImmediate.restore();
                window.clearImmediate.restore();
            }
            if(window.fetch) {
                window.fetch.restore();
            }
            window.XMLHttpRequest.prototype.open = oldOpen;

            document.removeEventListener(events.transitionstart, startHandler);
            document.removeEventListener(events.transitionend, endHandler);

            document.removeEventListener(events.animationstart, startHandler);
            document.removeEventListener(events.animationend, endHandler);

            if(animate) {
                Element.prototype.animate = animate;
            }

        }
    };

};

if (typeof window === 'undefined') {
    module.exports = instrumentBrowser;
}
