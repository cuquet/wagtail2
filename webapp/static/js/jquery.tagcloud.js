/*
 * jQuery TagCloud 0.5.0
 * Copyright (c) 2008 Ron Valstar
 * Dual licensed under the MIT and GPL licenses:
 *   http://www.opensource.org/licenses/mit-license.php
 *   http://www.gnu.org/licenses/gpl.html
 *   http://www.aharrisbooks.net/jad/chap_15/extensions/tagcloud/
 */
(function($) {
    var C;
    var A = {};
    var G = {};
    var L = 2.399963;
    $.fn.tagcloud = function(M) {
            C = $.extend({}, $.fn.tagcloud.defaults, M);
            if (C.seed === null) {
                C.seed = Math.ceil(Math.random() * 45309714203)
            }
            switch (C.type) {
                case "sphere":
                case "cloud":
                    A = {
                        position: "relative"
                    };
                    G = {
                        position: "absolute",
                        display: "block"
                    };
                    break;
                case "list":
                    A = {
                        height: "auto"
                    };
                    G = {
                        position: "static",
                        display: "inline"
                    };
                    break
            }
            B.setSeed(C.seed + 123456);
            return this.each(function(f, a) {
                var q = $(a);
                var R = q.find(">li");
                var S = R.length;
                var Z = q.width();
                var l = C.height === null ? (0.004 * Z * S) : C.height;
                q.css({
                    width: Z,
                    height: l,
                    listStyle: "none",
                    margin: 0,
                    padding: 0
                });
                q.css(A);
                var e = -2147483647;
                var r = 2147483648;
                var T = -1;
                for (var d = 0; d < S; d++) {
                    var p = $(R[d]);
                    var n = p.attr("value") == -1 ? T++ : p.attr("value");
                    if (n > e) {
                        e = n
                    }
                    if (n < r) {
                        r = n
                    }
                    T = n
                }
                var b = e - r;
                var X = new Array();
                for (var d = 0; d < S; d++) {
                    X[d] = d
                }
                for (var d, V, c = X.length; c; d = parseInt(B.rand(0, 1000) / 1000 * c), V = X[--c], X[c] = X[d], X[d] = V) {}
                T = -1;
                for (var d = 0; d < S; d++) {
                    var p = $(R[d]);
                    var n = p.attr("value") == -1 ? T++ : p.attr("value");
                    T = n;
                    var g = ((S - d - 1) / (S - 1));
                    var g = (n - r) / b;
                    var m = C.sizemin + g * (C.sizemax - C.sizemin);
                    var N = D(C.colormin, C.colormax, g);
                    p.css({
                        fontSize: m,
                        position: "absolute",
                        color: "#" + N,
                        margin: 0,
                        padding: 0
                    }).children().css({
                        color: "#" + N
                    });
                    var Y = p.width();
                    var h = p.height();
                    var Q = {};
                    if (C.type != "list") {
                        if (C.type == "cloud") {
                            var s = B.rand(0, Z - Y);
                            var W = X[d] * (l / S) - h / 2
                        } else {
                            var P = Math.pow(d / S, C.power);
                            var U = (d + Math.PI / 2) * L;
                            var s = Z / 2 - Y / 2 + 0.5 * Z * P * Math.sin(U);
                            var W = l / 2 - h / 2 + 0.5 * l * P * Math.cos(U)
                        }
                        Q.left = s;
                        Q.top = W
                    }
                    for (var O in G) {
                        Q[O] = G[O]
                    }
                    p.css(Q)
                }
            })
    };
    $.fn.tagcloud.defaults = {
        height: null,
        type: "cloud",
        sizemax: 20,
        sizemin: 10,
        colormax: "00F",
        colormin: "B4D2FF",
        seed: null,
        power: 0.5
    };
    var B = new function() {
        this.seed = 23145678901;
        this.A = 48271;
        this.M = 2147483647;
        this.Q = this.M / this.A;
        this.R = this.M % this.A;
        this.oneOverM = 1 / this.M
    };
    B.setSeed = function(M) {
        this.seed = M
    };
    B.next = function() {
        var M = this.seed / this.Q;
        var N = this.seed % this.Q;
        var O = this.A * N - this.R * M;
        this.seed = O + (O > 0 ? 0 : this.M);
        return (this.seed * this.oneOverM)
    };
    B.rand = function(N, M) {
        return Math.floor((M - N + 1) * this.next() + N)
    };

    function I(M) {
        return M.toString(16)
    }

    function K(M) {
        return parseInt(M, 16)
    }

    function H(Q) {
        var M = Q.length == 3;
        var O = [];
        for (var N = 0; N < 3; N++) {
            var P = Q.substring(N * (M ? 1 : 2), (N + 1) * (M ? 1 : 2));
            O.push(K(M ? P + P : P))
        }
        return O
    }

    function J(M) {
        var O = "";
        for (var N = 0; N < 3; N++) {
            var P = I(M[N]);
            if (P.length == 1) {
                P = "0" + P
            }
            O += P
        }
        return O
    }

    function D(R, S, P) {
        var Q = H(R);
        var M = H(S);
        var O = [];
        for (var N = 0; N < 3; N++) {
            O.push(Q[N] + Math.floor(P * (M[N] - Q[N])))
        }
        return J(O)
    }

    function E(M) {
        if (window.console && window.console.log) {
            if (typeof(M) == "string") {
                window.console.log(M)
            } else {
                for (var N in M) {
                    window.console.log(N + ": " + M[N])
                }
            }
        }
    }
})(jQuery);