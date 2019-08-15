/*! testability.js - v0.3.1
 *  Release on: 2016-10-11
 *  Copyright (c) 2016 Alfonso Presa
 *  Licensed MIT */
(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    // AMD. Register as an anonymous module unless amdModuleId is set
    define([], function () {
      return (root['testability'] = factory());
    });
  } else if (typeof exports === 'object') {
    // Node. Does not work with strict CommonJS, but
    // only CommonJS-like environments that support module.exports,
    // like Node.
    module.exports = factory();
  } else {
    root['testability'] = factory();
  }
}(this, function () {

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

return testability;

}));
