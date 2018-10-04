'use strict';

/*exported testability*/
var testability = (function Testability () {

    if (!this || this.constructor !==  Testability) {
        return new Testability();
    }

    var pendingCount = 0;
    var pendingCallbacks = [];

    this.reset = function () {
        pendingCount = 0;
        pendingCallbacks = [];
    };

    this.when = {
        ready: function (callback) {
            if (pendingCount === 0) {
                callback();
            }
            else {
                pendingCallbacks.push(callback);
            }
        }
    };

    this.wait = {
        start: function () {
            var self = this;
            this.oneMore();
            return {
                end: function () {
                    if (self) {
                        self.oneLess();
                    }
                    self = undefined;
                }
            };
        },
        oneMore: function () {
            pendingCount += 1;
        },
        oneLess: function () {
            pendingCount -= 1;
            if (pendingCount < 0) {
                pendingCount = 0;
            }
            if (pendingCount === 0) {
                while (pendingCount === 0 && pendingCallbacks.length !== 0) {
                    pendingCallbacks.pop()();
                }
            }
        },
        for: function (promise) {
            this.oneMore();
            promise.then(this.oneLess).catch(this.oneLess);
        }
    };

})();

