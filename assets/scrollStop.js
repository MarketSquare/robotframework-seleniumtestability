exports.scrollStop = function() {
  var isScrolling = null;
  window.addEventListener('scroll', function (event) {
    if (isScrolling != null) {
      window.clearTimeout(isScrolling);
      window.testability.wait.oneLess()
    }
    window.testability.wait.oneMore()
    isScrolling = setTimeout(function() {
      window.testability.wait.oneLess();
      isScrolling = null
    }, 66);
  }, false);
};
