(function(root, factory) {
	'use strict';
	var api = factory();
	if (typeof module === 'object' && module.exports) {
		module.exports = api;
	} else {
		root.PythonCourseSyntax = api;
	}
})(typeof globalThis !== 'undefined' ? globalThis : this, function() {
	'use strict';

	var aliases = {
		console: 'text',
		html: 'markup',
		js: 'javascript',
		md: 'markdown',
		py: 'python',
		shell: 'bash',
		sh: 'bash',
		txt: 'text',
		xml: 'markup',
		yml: 'yaml'
	};

	var grammars = {
		python: {
			flags: 'gi',
			rules: [
				['comment', '#[^\r\n]*'],
				['string', '(?:\\b[rubf]{1,2})?(?:"""[\\s\\S]*?"""|\\\'\\\'\\\'[\\s\\S]*?\\\'\\\'\\\'|"(?:\\\\.|[^"\\\\\\r\\n])*"|\\\'(?:\\\\.|[^\\\'\\\\\\r\\n])*\\\')'],
				['decorator', '@[a-z_]\\w*(?:\\.[a-z_]\\w*)*'],
				['number', '\\b(?:0[xob][\\da-f]+|\\d+(?:\\.\\d+)?(?:e[+-]?\\d+)?j?)\\b'],
				['keyword', '\\b(?:and|as|assert|async|await|break|case|class|continue|def|del|elif|else|except|exec|finally|for|from|global|if|import|in|is|lambda|match|nonlocal|not|or|pass|raise|return|try|while|with|yield)\\b'],
				['boolean', '\\b(?:false|none|true)\\b'],
				['builtin', '\\b(?:abs|all|any|bool|bytes|callable|chr|dict|dir|divmod|enumerate|eval|filter|float|format|frozenset|getattr|hasattr|hash|help|hex|id|input|int|isinstance|issubclass|iter|len|list|map|max|memoryview|min|next|object|oct|open|ord|pow|print|property|range|repr|reversed|round|set|setattr|slice|sorted|str|sum|super|tuple|type|vars|zip)\\b'],
				['function', '\\b[a-z_]\\w*(?=\\s*\\()'],
				['operator', '(?:\\*\\*|//|<<|>>|:=|==|!=|<=|>=|[-+%=<>*/&|^~])']
			]
		},
		javascript: {
			flags: 'g',
			rules: [
				['comment', '/\\*[\\s\\S]*?\\*/|//[^\r\n]*'],
				['string', '`(?:\\\\[\\s\\S]|[^`\\\\])*`|"(?:\\\\.|[^"\\\\\\r\\n])*"|\\\'(?:\\\\.|[^\\\'\\\\\\r\\n])*\\\''],
				['regex', '/(?![*/])(?:\\\\.|[^/\\\\\\r\\n])+/[dgimsuvy]*'],
				['number', '\\b(?:0[xob][\\da-f]+|\\d+(?:\\.\\d+)?(?:e[+-]?\\d+)?)n?\\b'],
				['keyword', '\\b(?:as|async|await|break|case|catch|class|const|continue|debugger|default|delete|do|else|export|extends|finally|for|from|function|get|if|implements|import|in|instanceof|interface|let|new|of|package|private|protected|public|return|set|static|super|switch|throw|try|typeof|var|void|while|with|yield)\\b'],
				['boolean', '\\b(?:false|null|true|undefined)\\b'],
				['builtin', '\\b(?:Array|BigInt|Boolean|Date|Error|JSON|Map|Math|Number|Object|Promise|RegExp|Set|String|Symbol|WeakMap|WeakSet|console|document|globalThis|window)\\b'],
				['function', '\\b[A-Za-z_$][\\w$]*(?=\\s*\\()'],
				['operator', '(?:=>|===?|!==?|\\*\\*|&&|\\|\\||\\?\\?|\\?\\.|[+%*/&|^!~?:=-])']
			]
		},
		bash: {
			flags: 'g',
			rules: [
				['comment', '#[^\r\n]*'],
				['string', '"(?:\\\\.|[^"\\\\\\r\\n])*"|\\\'(?:[^\\\'\\r\\n])*\\\''],
				['variable', '\\$(?:[A-Za-z_][A-Za-z0-9_]*|\\{[^}]+\\}|[?#@*!$0-9-])'],
				['keyword', '\\b(?:case|coproc|do|done|elif|else|esac|fi|for|function|if|in|select|then|time|until|while)\\b'],
				['builtin', '\\b(?:alias|cd|command|echo|eval|exec|exit|export|getopts|printf|pwd|read|readonly|set|shift|source|test|trap|type|ulimit|umask|unalias|unset)\\b'],
				['number', '\\b\\d+\\b'],
				['operator', '(?:&&|\\|\\||<<-?|>>?|[|&;])']
			]
		},
		yaml: {
			flags: 'gim',
			rules: [
				['comment', '#[^\r\n]*'],
				['string', '"(?:\\\\.|[^"\\\\\\r\\n])*"|\\\'(?:\\\'\\\'|[^\\\'\\r\\n])*\\\''],
				['property', '^[ \\t-]*[A-Za-z0-9_.-]+(?=\\s*:)'],
				['variable', '[&*!][A-Za-z0-9_.-]+'],
				['boolean', '\\b(?:false|null|true|yes|no|on|off|~)\\b'],
				['number', '\\b[-+]?(?:0[xob][\\da-f]+|\\d+(?:\\.\\d+)?)\\b'],
				['operator', '---|\\.\\.\\.|[|>:?\\[\\]{},-]']
			]
		},
		toml: {
			flags: 'gim',
			rules: [
				['comment', '#[^\r\n]*'],
				['string', '"""[\\s\\S]*?"""|\\\'\\\'\\\'[\\s\\S]*?\\\'\\\'\\\'|"(?:\\\\.|[^"\\\\\\r\\n])*"|\\\'(?:[^\\\'\\r\\n])*\\\''],
				['property', '^[ \\t]*[A-Za-z0-9_.-]+(?=\\s*=)'],
				['section', '^\\s*\\[\\[?[^\\]\r\n]+\\]\\]?'],
				['boolean', '\\b(?:false|true)\\b'],
				['number', '\\b[-+]?(?:0[xob][\\da-f_]+|\\d[\\d_]*(?:\\.[\\d_]+)?)\\b'],
				['operator', '[=\\[\\]{},]']
			]
		},
		sql: {
			flags: 'gi',
			rules: [
				['comment', '--[^\r\n]*|/\\*[\\s\\S]*?\\*/'],
				['string', '"(?:""|[^"])*"|\\\'(?:\\\'\\\'|[^\\\'])*\\\'|`(?:``|[^`])*`'],
				['keyword', '\\b(?:add|all|alter|and|as|asc|between|by|case|check|column|constraint|create|database|default|delete|desc|distinct|drop|else|end|exists|foreign|from|full|group|having|in|index|inner|insert|into|is|join|key|left|like|limit|not|null|on|or|order|outer|primary|references|right|row|select|set|table|then|union|unique|update|values|view|when|where|with)\\b'],
				['boolean', '\\b(?:false|null|true)\\b'],
				['function', '\\b[A-Za-z_]\\w*(?=\\s*\\()'],
				['number', '\\b(?:0x[\\da-f]+|\\d+(?:\\.\\d+)?)\\b'],
				['operator', '<>|!=|<=|>=|:=|[-+%=<>*/]']
			]
		},
		makefile: {
			flags: 'gim',
			rules: [
				['comment', '#[^\r\n]*'],
				['variable', '\\$(?:\\([^\\r\\n)]+\\)|\\{[^\\r\\n}]+\\}|[@%<?^+*])'],
				['property', '^[^\\s:#=]+(?=\\s*:)'],
				['keyword', '^\\s*(?:define|else|endef|endif|export|ifn?def|ifn?eq|include|override|private|sinclude|undefine|unexport|vpath)(?=\\s|$)'],
				['builtin', '\\b(?:addprefix|addsuffix|basename|call|dir|error|eval|filter|filter-out|findstring|firstword|flavor|foreach|join|lastword|notdir|origin|patsubst|realpath|shell|sort|strip|subst|suffix|value|warning|wildcard|word|wordlist|words)\\b'],
				['operator', '::?=|[?+!]?=|[|;]']
			]
		},
		markdown: {
			flags: 'gim',
			rules: [
				['comment', '<!--[\\s\\S]*?-->'],
				['keyword', '^#{1,6}(?=\\s)|^\\s*>|^\\s*(?:[-+*]|\\d+\\.)\\s+'],
				['code', '`{1,2}[^`]+`{1,2}'],
				['important', '\\*\\*[^*\\r\\n]+\\*\\*|__[^_\\r\\n]+__'],
				['emphasis', '(?:^|\\s)[*_][^*_\\r\\n]+[*_]'],
				['url', '!?\\[[^\\]\r\n]*\\]\\([^\\s)]+(?:\\s+"[^"]*")?\\)'],
				['tag', '</?[A-Za-z][^>]*>'],
				['operator', '^\\s*(?:---+|===+|```+|~~~+)\\s*$']
			]
		},
		markup: {
			flags: 'gi',
			rules: [
				['comment', '<!--[\\s\\S]*?-->'],
				['doctype', '<!DOCTYPE(?:[^>]|"[^"]*"|\\\'[^\\\']*\\\')+>'],
				['tag', '</?[A-Za-z][^>]*>'],
				['entity', '&(?:#x?[\\da-f]+|[A-Za-z][A-Za-z0-9]+);']
			]
		},
		css: {
			flags: 'gi',
			rules: [
				['comment', '/\\*[\\s\\S]*?\\*/'],
				['string', '"(?:\\\\.|[^"\\\\\\r\\n])*"|\\\'(?:\\\\.|[^\\\'\\\\\\r\\n])*\\\''],
				['atrule', '@[A-Za-z-]+'],
				['property', '--?[A-Za-z][A-Za-z0-9-]*(?=\\s*:)'],
				['number', '\\b\\d+(?:\\.\\d+)?(?:%|ch|cm|deg|em|ex|fr|in|mm|ms|pc|pt|px|rem|s|vh|vmax|vmin|vw)?\\b'],
				['important', '!important\\b'],
				['operator', '[{}:;,>+~]']
			]
		},
		json: {
			flags: 'g',
			rules: [
				['property', '"(?:\\\\.|[^"\\\\\\r\\n])*"(?=\\s*:)'],
				['string', '"(?:\\\\.|[^"\\\\\\r\\n])*"'],
				['boolean', '\\b(?:false|null|true)\\b'],
				['number', '-?\\b\\d+(?:\\.\\d+)?(?:e[+-]?\\d+)?\\b'],
				['operator', '[{}\\[\\],:]']
			]
		},
		java: {
			flags: 'g',
			rules: [
				['comment', '/\\*[\\s\\S]*?\\*/|//[^\r\n]*'],
				['string', '"(?:\\\\.|[^"\\\\\\r\\n])*"|\\\'(?:\\\\.|[^\\\'\\\\\\r\\n])*\\\''],
				['annotation', '@[A-Za-z_$][\\w$]*(?:\\.[A-Za-z_$][\\w$]*)*'],
				['keyword', '\\b(?:abstract|assert|boolean|break|byte|case|catch|char|class|const|continue|default|do|double|else|enum|exports|extends|final|finally|float|for|goto|if|implements|import|instanceof|int|interface|long|module|native|new|non-sealed|open|opens|package|permits|private|protected|provides|public|record|requires|return|sealed|short|static|strictfp|super|switch|synchronized|this|throw|throws|to|transient|transitive|try|uses|var|void|volatile|while|with|yield)\\b'],
				['boolean', '\\b(?:false|null|true)\\b'],
				['class-name', '\\b[A-Z][A-Za-z0-9_$]*\\b'],
				['function', '\\b[A-Za-z_$][\\w$]*(?=\\s*\\()'],
				['number', '\\b(?:0[xob][\\da-f_]+|\\d[\\d_]*(?:\\.[\\d_]+)?[dfl]?)\\b'],
				['operator', '>>>?=?|<<=?|->|::|&&|\\|\\||[-+%*/&|^!~?:=<>]=?']
			]
		}
	};

	function escapeHtml(value) {
		return String(value)
			.replace(/&/g, '&amp;')
			.replace(/</g, '&lt;')
			.replace(/>/g, '&gt;')
			.replace(/"/g, '&quot;');
	}

	function normalizeLanguage(language) {
		var clean = String(language || 'text').toLowerCase().replace(/^language-/, '').replace(/[^a-z0-9_-]/g, '');
		return aliases[clean] || clean || 'text';
	}

	function compiledGrammar(language) {
		var grammar = grammars[language];
		if (!grammar) {
			return null;
		}
		var source = grammar.rules.map(function(rule) { return '(' + rule[1] + ')'; }).join('|');
		return {
			rules: grammar.rules,
			pattern: new RegExp(source, grammar.flags)
		};
	}

	function highlight(source, language) {
		var normalized = normalizeLanguage(language);
		var grammar = compiledGrammar(normalized);
		if (!grammar) {
			return escapeHtml(source);
		}

		var html = '';
		var cursor = 0;
		String(source).replace(grammar.pattern, function(match) {
			var offset = arguments[arguments.length - 2];
			var type = 'plain';
			for (var i = 1; i <= grammar.rules.length; i += 1) {
				if (arguments[i] !== undefined) {
					type = grammar.rules[i - 1][0];
					break;
				}
			}
			html += escapeHtml(String(source).slice(cursor, offset));
			html += '<span class="syntax-' + type + '">' + escapeHtml(match) + '</span>';
			cursor = offset + match.length;
			return match;
		});
		html += escapeHtml(String(source).slice(cursor));
		return html;
	}

	return {
		highlight: highlight,
		normalizeLanguage: normalizeLanguage,
		supportedLanguages: Object.keys(grammars)
	};
});
