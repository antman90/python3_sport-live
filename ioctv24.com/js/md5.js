MD5 = function(e) {
    
    function h(a, b) {
        var c, d, e, f, g;
        e = a & 2147483648;
        f = b & 2147483648;
        c = a & 1073741824;
        d = b & 1073741824;
        g = (a & 1073741823) + (b & 1073741823);
        return c & d ? g ^ 2147483648 ^ e ^ f : c | d ? g & 1073741824 ? g ^ 3221225472 ^ e ^ f : g ^ 1073741824 ^ e ^ f : g ^ e ^ f
    }

    function k(a, b, c, d, e, f, g) {
        a = h(a, h(h(b & c | ~b & d, e), g));
        return h(a << f | a >>> 32 - f, b)
    }

    function l(a, b, c, d, e, f, g) {
        a = h(a, h(h(b & d | c & ~d, e), g));
        return h(a << f | a >>> 32 - f, b)
    }

    function m(a, b, d, c, e, f, g) {
        a = h(a, h(h(b ^ d ^ c, e), g));
        return h(a << f | a >>> 32 - f, b)
    }

    function n(a, b, d, c, e, f, g) {
        a = h(a, h(h(d ^ (b | ~c), e), g));
        return h(a << f | a >>> 32 - f, b)
    }

    function p(a) {
        var b = "",
            d = "",
            c;
        for (c = 0; 3 >= c; c++) d = a >>> 8 * c & 255, d = "0" + d.toString(16), b += d.substr(d.length - 2, 2);
        return b
    }
    var f = [],
        q, r, s, t, a, b, c, d;
    e = function(a) {
        a = a.replace(/\r\n/g, "\n");
        for (var b = "", d = 0; d < a.length; d++) {
            var c = a.charCodeAt(d);
            128 > c ? b += String.fromCharCode(c) : (127 < c && 2048 > c ? b += String.fromCharCode(c >> 6 | 192) : (b += String.fromCharCode(c >> 12 | 224), b += String.fromCharCode(c >> 6 & 63 | 128)), b += String.fromCharCode(c & 63 | 128))
        }
        return b
    }(e);
    f = function(b) {
        var a, c = b.length;
        a = c + 8;
        for (var d = 16 * ((a - a % 64) / 64 + 1), e = Array(d - 1), f = 0, g = 0; g < c;) a = (g - g % 4) / 4, f = g % 4 * 8, e[a] |= b.charCodeAt(g) << f, g++;
        a = (g - g % 4) / 4;
        e[a] |= 128 << g % 4 * 8;
        e[d - 2] = c << 3;
        e[d - 1] = c >>> 29;
        return e
    }(e);
    a = 1732584193;
    b = 4023233417;
    c = 2562383102;
    d = 271733878;
    for (e = 0; e < f.length; e += 16) q = a, r = b, s = c, t = d, a = k(a, b, c, d, f[e + 0], 7, 3614090360), d = k(d, a, b, c, f[e + 1], 12, 3905402710), c = k(c, d, a, b, f[e + 2], 17, 606105819), b = k(b, c, d, a, f[e + 3], 22, 3250441966), a = k(a, b, c, d, f[e + 4], 7, 4118548399), d = k(d, a, b, c, f[e + 5], 12, 1200080426), c = k(c, d, a, b, f[e + 6], 17, 2821735955), b = k(b, c, d, a, f[e + 7], 22, 4249261313), a = k(a, b, c, d, f[e + 8], 7, 1770035416), d = k(d, a, b, c, f[e + 9], 12, 2336552879), c = k(c, d, a, b, f[e + 10], 17, 4294925233), b = k(b, c, d, a, f[e + 11], 22, 2304563134), a = k(a, b, c, d, f[e + 12], 7, 1804603682), d = k(d, a, b, c, f[e + 13], 12, 4254626195), c = k(c, d, a, b, f[e + 14], 17, 2792965006), b = k(b, c, d, a, f[e + 15], 22, 1236535329), a = l(a, b, c, d, f[e + 1], 5, 4129170786), d = l(d, a, b, c, f[e + 6], 9, 3225465664), c = l(c, d, a, b, f[e + 11], 14, 643717713), b = l(b, c, d, a, f[e + 0], 20, 3921069994), a = l(a, b, c, d, f[e + 5], 5, 3593408605), d = l(d, a, b, c, f[e + 10], 9, 38016083), c = l(c, d, a, b, f[e + 15], 14, 3634488961), b = l(b, c, d, a, f[e + 4], 20, 3889429448), a = l(a, b, c, d, f[e + 9], 5, 568446438), d = l(d, a, b, c, f[e + 14], 9, 3275163606), c = l(c, d, a, b, f[e + 3], 14, 4107603335), b = l(b, c, d, a, f[e + 8], 20, 1163531501), a = l(a, b, c, d, f[e + 13], 5, 2850285829), d = l(d, a, b, c, f[e + 2], 9, 4243563512), c = l(c, d, a, b, f[e + 7], 14, 1735328473), b = l(b, c, d, a, f[e + 12], 20, 2368359562), a = m(a, b, c, d, f[e + 5], 4, 4294588738), d = m(d, a, b, c, f[e + 8], 11, 2272392833), c = m(c, d, a, b, f[e + 11], 16, 1839030562), b = m(b, c, d, a, f[e + 14], 23, 4259657740), a = m(a, b, c, d, f[e + 1], 4, 2763975236), d = m(d, a, b, c, f[e + 4], 11, 1272893353), c = m(c, d, a, b, f[e + 7], 16, 4139469664), b = m(b, c, d, a, f[e + 10], 23, 3200236656), a = m(a, b, c, d, f[e + 13], 4, 681279174), d = m(d, a, b, c, f[e + 0], 11, 3936430074), c = m(c, d, a, b, f[e + 3], 16, 3572445317), b = m(b, c, d, a, f[e + 6], 23, 76029189), a = m(a, b, c, d, f[e + 9], 4, 3654602809), d = m(d, a, b, c, f[e + 12], 11, 3873151461), c = m(c, d, a, b, f[e + 15], 16, 530742520), b = m(b, c, d, a, f[e + 2], 23, 3299628645), a = n(a, b, c, d, f[e + 0], 6, 4096336452), d = n(d, a, b, c, f[e + 7], 10, 1126891415), c = n(c, d, a, b, f[e + 14], 15, 2878612391), b = n(b, c, d, a, f[e + 5], 21, 4237533241), a = n(a, b, c, d, f[e + 12], 6, 1700485571), d = n(d, a, b, c, f[e + 3], 10, 2399980690), c = n(c, d, a, b, f[e + 10], 15, 4293915773), b = n(b, c, d, a, f[e + 1], 21, 2240044497), a = n(a, b, c, d, f[e + 8], 6, 1873313359), d = n(d, a, b, c, f[e + 15], 10, 4264355552), c = n(c, d, a, b, f[e + 6], 15, 2734768916), b = n(b, c, d, a, f[e + 13], 21, 1309151649), a = n(a, b, c, d, f[e + 4], 6, 4149444226), d = n(d, a, b, c, f[e + 11], 10, 3174756917), c = n(c, d, a, b, f[e + 2], 15, 718787259), b = n(b, c, d, a, f[e + 9], 21, 3951481745), a = h(a, q), b = h(b, r), c = h(c, s), d = h(d, t);
    return (p(a) + p(b) + p(c) + p(d)).toLowerCase()
};

// if (typeof(MD5_JS) == 'undefined') // 한번만 실행
// {
//     var MD5_JS = true;

//     /* See http://pajhome.org.uk/crypt/md5 for more info  */
//     var hexcase = 0;
//     var b64pad  = "";
//     var chrsz   = 8;

//     function hex_md5(s){ return binl2hex(core_md5(str2binl(s), s.length * chrsz));}
//     function b64_md5(s){ return binl2b64(core_md5(str2binl(s), s.length * chrsz));}
//     function str_md5(s){ return binl2str(core_md5(str2binl(s), s.length * chrsz));}
//     function hex_hmac_md5(key, data) { return binl2hex(core_hmac_md5(key, data)); }
//     function b64_hmac_md5(key, data) { return binl2b64(core_hmac_md5(key, data)); }
//     function str_hmac_md5(key, data) { return binl2str(core_hmac_md5(key, data)); }

//     function core_md5(x, len) 
//     {
//         x[len >> 5] |= 0x80 << ((len) % 32); x[(((len + 64) >>> 9) << 4) + 14] = len;
//         var a =  1732584193; var b = -271733879; var c = -1732584194; var d =  271733878;
//         for(var i = 0; i < x.length; i += 16) 
//         {
//             var olda = a; var oldb = b; var oldc = c; var oldd = d;
//             a = md5_ff(a, b, c, d, x[i+ 0], 7 , -680876936);
//             d = md5_ff(d, a, b, c, x[i+ 1], 12, -389564586);
//             c = md5_ff(c, d, a, b, x[i+ 2], 17,  606105819);
//             b = md5_ff(b, c, d, a, x[i+ 3], 22, -1044525330);
//             a = md5_ff(a, b, c, d, x[i+ 4], 7 , -176418897);
//             d = md5_ff(d, a, b, c, x[i+ 5], 12,  1200080426);
//             c = md5_ff(c, d, a, b, x[i+ 6], 17, -1473231341);
//             b = md5_ff(b, c, d, a, x[i+ 7], 22, -45705983);
//             a = md5_ff(a, b, c, d, x[i+ 8], 7 ,  1770035416);
//             d = md5_ff(d, a, b, c, x[i+ 9], 12, -1958414417);
//             c = md5_ff(c, d, a, b, x[i+10], 17, -42063);
//             b = md5_ff(b, c, d, a, x[i+11], 22, -1990404162);
//             a = md5_ff(a, b, c, d, x[i+12], 7 ,  1804603682);
//             d = md5_ff(d, a, b, c, x[i+13], 12, -40341101);
//             c = md5_ff(c, d, a, b, x[i+14], 17, -1502002290);
//             b = md5_ff(b, c, d, a, x[i+15], 22,  1236535329);

//             a = md5_gg(a, b, c, d, x[i+ 1], 5 , -165796510);
//             d = md5_gg(d, a, b, c, x[i+ 6], 9 , -1069501632);
//             c = md5_gg(c, d, a, b, x[i+11], 14,  643717713);
//             b = md5_gg(b, c, d, a, x[i+ 0], 20, -373897302);
//             a = md5_gg(a, b, c, d, x[i+ 5], 5 , -701558691);
//             d = md5_gg(d, a, b, c, x[i+10], 9 ,  38016083);
//             c = md5_gg(c, d, a, b, x[i+15], 14, -660478335);
//             b = md5_gg(b, c, d, a, x[i+ 4], 20, -405537848);
//             a = md5_gg(a, b, c, d, x[i+ 9], 5 ,  568446438);
//             d = md5_gg(d, a, b, c, x[i+14], 9 , -1019803690);
//             c = md5_gg(c, d, a, b, x[i+ 3], 14, -187363961);
//             b = md5_gg(b, c, d, a, x[i+ 8], 20,  1163531501);
//             a = md5_gg(a, b, c, d, x[i+13], 5 , -1444681467);
//             d = md5_gg(d, a, b, c, x[i+ 2], 9 , -51403784);
//             c = md5_gg(c, d, a, b, x[i+ 7], 14,  1735328473);
//             b = md5_gg(b, c, d, a, x[i+12], 20, -1926607734);

//             a = md5_hh(a, b, c, d, x[i+ 5], 4 , -378558);
//             d = md5_hh(d, a, b, c, x[i+ 8], 11, -2022574463);
//             c = md5_hh(c, d, a, b, x[i+11], 16,  1839030562);
//             b = md5_hh(b, c, d, a, x[i+14], 23, -35309556);
//             a = md5_hh(a, b, c, d, x[i+ 1], 4 , -1530992060);
//             d = md5_hh(d, a, b, c, x[i+ 4], 11,  1272893353);
//             c = md5_hh(c, d, a, b, x[i+ 7], 16, -155497632);
//             b = md5_hh(b, c, d, a, x[i+10], 23, -1094730640);
//             a = md5_hh(a, b, c, d, x[i+13], 4 ,  681279174);
//             d = md5_hh(d, a, b, c, x[i+ 0], 11, -358537222);
//             c = md5_hh(c, d, a, b, x[i+ 3], 16, -722521979);
//             b = md5_hh(b, c, d, a, x[i+ 6], 23,  76029189);
//             a = md5_hh(a, b, c, d, x[i+ 9], 4 , -640364487);
//             d = md5_hh(d, a, b, c, x[i+12], 11, -421815835);
//             c = md5_hh(c, d, a, b, x[i+15], 16,  530742520);
//             b = md5_hh(b, c, d, a, x[i+ 2], 23, -995338651);

//             a = md5_ii(a, b, c, d, x[i+ 0], 6 , -198630844);
//             d = md5_ii(d, a, b, c, x[i+ 7], 10,  1126891415);
//             c = md5_ii(c, d, a, b, x[i+14], 15, -1416354905);
//             b = md5_ii(b, c, d, a, x[i+ 5], 21, -57434055);
//             a = md5_ii(a, b, c, d, x[i+12], 6 ,  1700485571);
//             d = md5_ii(d, a, b, c, x[i+ 3], 10, -1894986606);
//             c = md5_ii(c, d, a, b, x[i+10], 15, -1051523);
//             b = md5_ii(b, c, d, a, x[i+ 1], 21, -2054922799);
//             a = md5_ii(a, b, c, d, x[i+ 8], 6 ,  1873313359);
//             d = md5_ii(d, a, b, c, x[i+15], 10, -30611744);
//             c = md5_ii(c, d, a, b, x[i+ 6], 15, -1560198380);
//             b = md5_ii(b, c, d, a, x[i+13], 21,  1309151649);
//             a = md5_ii(a, b, c, d, x[i+ 4], 6 , -145523070);
//             d = md5_ii(d, a, b, c, x[i+11], 10, -1120210379);
//             c = md5_ii(c, d, a, b, x[i+ 2], 15,  718787259);
//             b = md5_ii(b, c, d, a, x[i+ 9], 21, -343485551);

//             a = safe_add(a, olda); b = safe_add(b, oldb); c = safe_add(c, oldc); d = safe_add(d, oldd);
//         }
//         return Array(a, b, c, d);
//     }

//     function md5_cmn(q, a, b, x, s, t) { return safe_add(bit_rol(safe_add(safe_add(a, q), safe_add(x, t)), s),b); }
//     function md5_ff(a, b, c, d, x, s, t) { return md5_cmn((b & c) | ((~b) & d), a, b, x, s, t); }
//     function md5_gg(a, b, c, d, x, s, t) { return md5_cmn((b & d) | (c & (~d)), a, b, x, s, t); }
//     function md5_hh(a, b, c, d, x, s, t) { return md5_cmn(b ^ c ^ d, a, b, x, s, t); }
//     function md5_ii(a, b, c, d, x, s, t) { return md5_cmn(c ^ (b | (~d)), a, b, x, s, t); }

//     function core_hmac_md5(key, data) {
//         var bkey = str2binl(key);
//         if(bkey.length > 16) 
//             bkey = core_md5(bkey, key.length * chrsz);

//         var ipad = Array(16), opad = Array(16);
//         for(var i = 0; i < 16; i++) 
//         { 
//             ipad[i] = bkey[i] ^ 0x36363636; 
//             opad[i] = bkey[i] ^ 0x5C5C5C5C; 
//         }

//         var hash = core_md5(ipad.concat(str2binl(data)), 512 + data.length * chrsz);
//         return core_md5(opad.concat(hash), 512 + 128);
//     }

//     function safe_add(x, y) { var lsw = (x & 0xFFFF) + (y & 0xFFFF); var msw = (x >> 16) + (y >> 16) + (lsw >> 16); return (msw << 16) | (lsw & 0xFFFF); }
//     function bit_rol(num, cnt) { return (num << cnt) | (num >>> (32 - cnt)); }

//     function str2binl(str) 
//     {
//         var bin = Array(); var mask = (1 << chrsz) - 1;
//         for(var i = 0; i < str.length * chrsz; i += chrsz) 
//             bin[i>>5] |= (str.charCodeAt(i / chrsz) & mask) << (i%32);
//         return bin; 
//     }

//     function binl2str(bin) 
//     {
//         var str = ""; var mask = (1 << chrsz) - 1;
//         for(var i = 0; i < bin.length * 32; i += chrsz) 
//             str += String.fromCharCode((bin[i>>5] >>> (i % 32)) & mask); return str; 
//     }


//     function binl2hex(binarray) 
//     {
//         var hex_tab = hexcase ? "0123456789ABCDEF" : "0123456789abcdef"; var str = "";
//         for(var i = 0; i < binarray.length * 4; i++) 
//             str += hex_tab.charAt((binarray[i>>2] >> ((i%4)*8+4)) & 0xF) + hex_tab.charAt((binarray[i>>2] >> ((i%4)*8  )) & 0xF); 
//         return str; 
//     }

//     function binl2b64(binarray) 
//     {
//         var tab = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
//         var str = "";
//         for(var i = 0; i < binarray.length * 4; i += 3) 
//         {
//             var triplet = (((binarray[i   >> 2] >> 8 * ( i   %4)) & 0xFF) << 16)
//                         | (((binarray[i+1 >> 2] >> 8 * ((i+1)%4)) & 0xFF) << 8 )
//                         |  ((binarray[i+2 >> 2] >> 8 * ((i+2)%4)) & 0xFF);
//             for(var j = 0; j < 4; j++) 
//             {
//                 if(i * 8 + j * 6 > binarray.length * 32) 
//                     str += b64pad;
//                 else 
//                     str += tab.charAt((triplet >> 6*(3-j)) & 0x3F); 
//             }
//         }
//         return str;
//     }
// }