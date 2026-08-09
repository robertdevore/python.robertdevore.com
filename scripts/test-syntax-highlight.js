'use strict';

var assert = require('node:assert/strict');
var syntax = require('../assets/js/syntax-highlight.js');

var cases = [
	['python', 'def greet(name):\n    # hello\n    print("Welcome")\n    return f"Hi {name}"', ['syntax-keyword', 'syntax-function', 'syntax-comment', 'syntax-builtin', 'syntax-string']],
	['javascript', 'const answer = Math.max(40, 2);', ['syntax-keyword', 'syntax-builtin', 'syntax-function', 'syntax-number']],
	['bash', 'echo "$HOME" # path', ['syntax-builtin', 'syntax-string', 'syntax-comment']],
	['yaml', 'enabled: true\ncount: 3', ['syntax-property', 'syntax-boolean', 'syntax-number']],
	['toml', '[tool.demo]\nenabled = true', ['syntax-section', 'syntax-property', 'syntax-boolean']],
	['sql', 'SELECT id FROM users WHERE active = true;', ['syntax-keyword', 'syntax-operator', 'syntax-boolean']],
	['markdown', '# Title\nUse **bold** and `code`.', ['syntax-keyword', 'syntax-important', 'syntax-code']],
	['makefile', 'build: $(SOURCES)\n\t$(CC) -o app', ['syntax-property', 'syntax-variable']],
	['java', 'public class Hello { public static void main() {} }', ['syntax-keyword', 'syntax-class-name', 'syntax-function']]
];

cases.forEach(function(testCase) {
	var language = testCase[0];
	var html = syntax.highlight(testCase[1], language);
	testCase[2].forEach(function(className) {
		assert.match(html, new RegExp('class="' + className + '"'), language + ' should emit ' + className);
	});
});

assert.equal(syntax.normalizeLanguage('language-py'), 'python');
assert.equal(syntax.normalizeLanguage('sh'), 'bash');
assert.equal(syntax.normalizeLanguage('md'), 'markdown');
assert.equal(syntax.highlight('<plain & safe>', 'text'), '&lt;plain &amp; safe&gt;');
assert.doesNotMatch(syntax.highlight('<script>alert(1)</script>', 'unknown'), /<script>/);

console.log('Syntax highlighting contract passed (' + cases.length + ' language grammars)');
