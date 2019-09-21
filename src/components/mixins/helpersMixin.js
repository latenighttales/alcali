export default {
  methods: {
    /* function to allow Salt-style globbing on event tags. */
    fnmatch(pattern) {
      if (pattern.indexOf('*') === -1) {
        return filename => pattern === filename;
      } else {
        let reRegExpChar = /[\\^$.*+?()[\]{}|]/g;
        let escaped = pattern.replace(reRegExpChar, '\\$&');
        let matcher = new RegExp('^' + escaped.replace(/\\\*/g, '.*') + '$');
        return filename => matcher.test(filename);
      }
    },
    sleep(milliseconds) {
      return new Promise(resolve => setTimeout(resolve, milliseconds))
    },
  }
};