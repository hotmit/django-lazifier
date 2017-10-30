(function(global){'use strict';var _Base64=global.Base64;var version="2.1.9";var buffer;if(typeof module!=='undefined'&&module.exports){try{buffer=require('buffer').Buffer;}catch(err){}}
var b64chars='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';var b64tab=function(bin){var t={};for(var i=0,l=bin.length;i<l;i++)t[bin.charAt(i)]=i;return t;}(b64chars);var fromCharCode=String.fromCharCode;var cb_utob=function(c){if(c.length<2){var cc=c.charCodeAt(0);return cc<0x80?c:cc<0x800?(fromCharCode(0xc0|(cc>>>6))
+fromCharCode(0x80|(cc&0x3f))):(fromCharCode(0xe0|((cc>>>12)&0x0f))
+fromCharCode(0x80|((cc>>>6)&0x3f))
+fromCharCode(0x80|(cc&0x3f)));}else{var cc=0x10000
+(c.charCodeAt(0)-0xD800)*0x400
+(c.charCodeAt(1)-0xDC00);return(fromCharCode(0xf0|((cc>>>18)&0x07))
+fromCharCode(0x80|((cc>>>12)&0x3f))
+fromCharCode(0x80|((cc>>>6)&0x3f))
+fromCharCode(0x80|(cc&0x3f)));}};var re_utob=/[\uD800-\uDBFF][\uDC00-\uDFFFF]|[^\x00-\x7F]/g;var utob=function(u){return u.replace(re_utob,cb_utob);};var cb_encode=function(ccc){var padlen=[0,2,1][ccc.length%3],ord=ccc.charCodeAt(0)<<16|((ccc.length>1?ccc.charCodeAt(1):0)<<8)|((ccc.length>2?ccc.charCodeAt(2):0)),chars=[b64chars.charAt(ord>>>18),b64chars.charAt((ord>>>12)&63),padlen>=2?'=':b64chars.charAt((ord>>>6)&63),padlen>=1?'=':b64chars.charAt(ord&63)];return chars.join('');};var btoa=global.btoa?function(b){return global.btoa(b);}:function(b){return b.replace(/[\s\S]{1,3}/g,cb_encode);};var _encode=buffer?function(u){return(u.constructor===buffer.constructor?u:new buffer(u)).toString('base64')}:function(u){return btoa(utob(u))};var encode=function(u,urisafe){return!urisafe?_encode(String(u)):_encode(String(u)).replace(/[+\/]/g,function(m0){return m0=='+'?'-':'_';}).replace(/=/g,'');};var encodeURI=function(u){return encode(u,true)};var re_btou=new RegExp(['[\xC0-\xDF][\x80-\xBF]','[\xE0-\xEF][\x80-\xBF]{2}','[\xF0-\xF7][\x80-\xBF]{3}'].join('|'),'g');var cb_btou=function(cccc){switch(cccc.length){case 4:var cp=((0x07&cccc.charCodeAt(0))<<18)|((0x3f&cccc.charCodeAt(1))<<12)|((0x3f&cccc.charCodeAt(2))<<6)|(0x3f&cccc.charCodeAt(3)),offset=cp-0x10000;return(fromCharCode((offset>>>10)+0xD800)
+fromCharCode((offset&0x3FF)+0xDC00));case 3:return fromCharCode(((0x0f&cccc.charCodeAt(0))<<12)|((0x3f&cccc.charCodeAt(1))<<6)|(0x3f&cccc.charCodeAt(2)));default:return fromCharCode(((0x1f&cccc.charCodeAt(0))<<6)|(0x3f&cccc.charCodeAt(1)));}};var btou=function(b){return b.replace(re_btou,cb_btou);};var cb_decode=function(cccc){var len=cccc.length,padlen=len%4,n=(len>0?b64tab[cccc.charAt(0)]<<18:0)|(len>1?b64tab[cccc.charAt(1)]<<12:0)|(len>2?b64tab[cccc.charAt(2)]<<6:0)|(len>3?b64tab[cccc.charAt(3)]:0),chars=[fromCharCode(n>>>16),fromCharCode((n>>>8)&0xff),fromCharCode(n&0xff)];chars.length-=[0,0,2,1][padlen];return chars.join('');};var atob=global.atob?function(a){return global.atob(a);}:function(a){return a.replace(/[\s\S]{1,4}/g,cb_decode);};var _decode=buffer?function(a){return(a.constructor===buffer.constructor?a:new buffer(a,'base64')).toString();}:function(a){return btou(atob(a))};var decode=function(a){return _decode(String(a).replace(/[-_]/g,function(m0){return m0=='-'?'+':'/'}).replace(/[^A-Za-z0-9\+\/]/g,''));};var noConflict=function(){var Base64=global.Base64;global.Base64=_Base64;return Base64;};global.Base64={VERSION:version,atob:atob,btoa:btoa,fromBase64:decode,toBase64:encode,utob:utob,encode:encode,encodeURI:encodeURI,btou:btou,decode:decode,noConflict:noConflict};if(typeof Object.defineProperty==='function'){var noEnum=function(v){return{value:v,enumerable:false,writable:true,configurable:true};};global.Base64.extendString=function(){Object.defineProperty(String.prototype,'fromBase64',noEnum(function(){return decode(this)}));Object.defineProperty(String.prototype,'toBase64',noEnum(function(urisafe){return encode(this,urisafe)}));Object.defineProperty(String.prototype,'toBase64URI',noEnum(function(){return encode(this,true)}));};}
if(global['Meteor']){Base64=global.Base64;}})(this);if(typeof JSON!=="object"){JSON={};}
(function(){"use strict";var rx_one=/^[\],:{}\s]*$/;var rx_two=/\\(?:["\\\/bfnrt]|u[0-9a-fA-F]{4})/g;var rx_three=/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g;var rx_four=/(?:^|:|,)(?:\s*\[)+/g;var rx_escapable=/[\\\"\u0000-\u001f\u007f-\u009f\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g;var rx_dangerous=/[\u0000\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g;function f(n){return n<10?"0"+n:n;}
function this_value(){return this.valueOf();}
if(typeof Date.prototype.toJSON!=="function"){Date.prototype.toJSON=function(){return isFinite(this.valueOf())?this.getUTCFullYear()+"-"+
f(this.getUTCMonth()+1)+"-"+
f(this.getUTCDate())+"T"+
f(this.getUTCHours())+":"+
f(this.getUTCMinutes())+":"+
f(this.getUTCSeconds())+"Z":null;};Boolean.prototype.toJSON=this_value;Number.prototype.toJSON=this_value;String.prototype.toJSON=this_value;}
var gap;var indent;var meta;var rep;function quote(string){rx_escapable.lastIndex=0;return rx_escapable.test(string)?"\""+string.replace(rx_escapable,function(a){var c=meta[a];return typeof c==="string"?c:"\\u"+("0000"+a.charCodeAt(0).toString(16)).slice(-4);})+"\"":"\""+string+"\"";}
function str(key,holder){var i;var k;var v;var length;var mind=gap;var partial;var value=holder[key];if(value&&typeof value==="object"&&typeof value.toJSON==="function"){value=value.toJSON(key);}
if(typeof rep==="function"){value=rep.call(holder,key,value);}
switch(typeof value){case"string":return quote(value);case"number":return isFinite(value)?String(value):"null";case"boolean":case"null":return String(value);case"object":if(!value){return"null";}
gap+=indent;partial=[];if(Object.prototype.toString.apply(value)==="[object Array]"){length=value.length;for(i=0;i<length;i+=1){partial[i]=str(i,value)||"null";}
v=partial.length===0?"[]":gap?"[\n"+gap+partial.join(",\n"+gap)+"\n"+mind+"]":"["+partial.join(",")+"]";gap=mind;return v;}
if(rep&&typeof rep==="object"){length=rep.length;for(i=0;i<length;i+=1){if(typeof rep[i]==="string"){k=rep[i];v=str(k,value);if(v){partial.push(quote(k)+(gap?": ":":")+v);}}}}else{for(k in value){if(Object.prototype.hasOwnProperty.call(value,k)){v=str(k,value);if(v){partial.push(quote(k)+(gap?": ":":")+v);}}}}
v=partial.length===0?"{}":gap?"{\n"+gap+partial.join(",\n"+gap)+"\n"+mind+"}":"{"+partial.join(",")+"}";gap=mind;return v;}}
if(typeof JSON.stringify!=="function"){meta={"\b":"\\b","\t":"\\t","\n":"\\n","\f":"\\f","\r":"\\r","\"":"\\\"","\\":"\\\\"};JSON.stringify=function(value,replacer,space){var i;gap="";indent="";if(typeof space==="number"){for(i=0;i<space;i+=1){indent+=" ";}}else if(typeof space==="string"){indent=space;}
rep=replacer;if(replacer&&typeof replacer!=="function"&&(typeof replacer!=="object"||typeof replacer.length!=="number")){throw new Error("JSON.stringify");}
return str("",{"":value});};}
if(typeof JSON.parse!=="function"){JSON.parse=function(text,reviver){var j;function walk(holder,key){var k;var v;var value=holder[key];if(value&&typeof value==="object"){for(k in value){if(Object.prototype.hasOwnProperty.call(value,k)){v=walk(value,k);if(v!==undefined){value[k]=v;}else{delete value[k];}}}}
return reviver.call(holder,key,value);}
text=String(text);rx_dangerous.lastIndex=0;if(rx_dangerous.test(text)){text=text.replace(rx_dangerous,function(a){return"\\u"+
("0000"+a.charCodeAt(0).toString(16)).slice(-4);});}
if(rx_one.test(text.replace(rx_two,"@").replace(rx_three,"]").replace(rx_four,""))){j=eval("("+text+")");return(typeof reviver==="function")?walk({"":j},""):j;}
throw new SyntaxError("JSON.parse");};}}());var FlashDetect=new function(){var self=this;self.installed=false;self.raw="";self.major=-1;self.minor=-1;self.revision=-1;self.revisionStr="";var activeXDetectRules=[{"name":"ShockwaveFlash.ShockwaveFlash.7","version":function(obj){return getActiveXVersion(obj);}},{"name":"ShockwaveFlash.ShockwaveFlash.6","version":function(obj){var version="6,0,21";try{obj.AllowScriptAccess="always";version=getActiveXVersion(obj);}catch(err){}
return version;}},{"name":"ShockwaveFlash.ShockwaveFlash","version":function(obj){return getActiveXVersion(obj);}}];var getActiveXVersion=function(activeXObj){var version=-1;try{version=activeXObj.GetVariable("$version");}catch(err){}
return version;};var getActiveXObject=function(name){var obj=-1;try{obj=new ActiveXObject(name);}catch(err){obj={activeXError:true};}
return obj;};var parseActiveXVersion=function(str){var versionArray=str.split(",");return{"raw":str,"major":parseInt(versionArray[0].split(" ")[1],10),"minor":parseInt(versionArray[1],10),"revision":parseInt(versionArray[2],10),"revisionStr":versionArray[2]};};var parseStandardVersion=function(str){var descParts=str.split(/ +/);var majorMinor=descParts[2].split(/\./);var revisionStr=descParts[3];return{"raw":str,"major":parseInt(majorMinor[0],10),"minor":parseInt(majorMinor[1],10),"revisionStr":revisionStr,"revision":parseRevisionStrToInt(revisionStr)};};var parseRevisionStrToInt=function(str){return parseInt(str.replace(/[a-zA-Z]/g,""),10)||self.revision;};self.majorAtLeast=function(version){return self.major>=version;};self.minorAtLeast=function(version){return self.minor>=version;};self.revisionAtLeast=function(version){return self.revision>=version;};self.versionAtLeast=function(major){var properties=[self.major,self.minor,self.revision];var len=Math.min(properties.length,arguments.length);for(i=0;i<len;i++){if(properties[i]>=arguments[i]){if(i+1<len&&properties[i]==arguments[i]){continue;}else{return true;}}else{return false;}}};self.FlashDetect=function(){if(navigator.plugins&&navigator.plugins.length>0){var type='application/x-shockwave-flash';var mimeTypes=navigator.mimeTypes;if(mimeTypes&&mimeTypes[type]&&mimeTypes[type].enabledPlugin&&mimeTypes[type].enabledPlugin.description){var version=mimeTypes[type].enabledPlugin.description;var versionObj=parseStandardVersion(version);self.raw=versionObj.raw;self.major=versionObj.major;self.minor=versionObj.minor;self.revisionStr=versionObj.revisionStr;self.revision=versionObj.revision;self.installed=true;}}else if(navigator.appVersion.indexOf("Mac")==-1&&window.execScript){var version=-1;for(var i=0;i<activeXDetectRules.length&&version==-1;i++){var obj=getActiveXObject(activeXDetectRules[i].name);if(!obj.activeXError){self.installed=true;version=activeXDetectRules[i].version(obj);if(version!=-1){var versionObj=parseActiveXVersion(version);self.raw=versionObj.raw;self.major=versionObj.major;self.minor=versionObj.minor;self.revision=versionObj.revision;self.revisionStr=versionObj.revisionStr;}}}}}();};FlashDetect.JS_RELEASE="1.0.4";(function(root,factory){'use strict';if(typeof exports==='object'){module.exports=factory(require('./punycode'),require('./IPv6'),require('./SecondLevelDomains'));}else if(typeof define==='function'&&define.amd){define(['./punycode','./IPv6','./SecondLevelDomains'],factory);}else{root.URI=factory(root.punycode,root.IPv6,root.SecondLevelDomains,root);}}(this,function(punycode,IPv6,SLD,root){'use strict';var _URI=root&&root.URI;function URI(url,base){var _urlSupplied=arguments.length>=1;var _baseSupplied=arguments.length>=2;if(!(this instanceof URI)){if(_urlSupplied){if(_baseSupplied){return new URI(url,base);}
return new URI(url);}
return new URI();}
if(url===undefined){if(_urlSupplied){throw new TypeError('undefined is not a valid argument for URI');}
if(typeof location!=='undefined'){url=location.href+'';}else{url='';}}
this.href(url);if(base!==undefined){return this.absoluteTo(base);}
return this;}
URI.version='1.17.1';var p=URI.prototype;var hasOwn=Object.prototype.hasOwnProperty;function escapeRegEx(string){return string.replace(/([.*+?^=!:${}()|[\]\/\\])/g,'\\$1');}
function getType(value){if(value===undefined){return'Undefined';}
return String(Object.prototype.toString.call(value)).slice(8,-1);}
function isArray(obj){return getType(obj)==='Array';}
function filterArrayValues(data,value){var lookup={};var i,length;if(getType(value)==='RegExp'){lookup=null;}else if(isArray(value)){for(i=0,length=value.length;i<length;i++){lookup[value[i]]=true;}}else{lookup[value]=true;}
for(i=0,length=data.length;i<length;i++){var _match=lookup&&lookup[data[i]]!==undefined||!lookup&&value.test(data[i]);if(_match){data.splice(i,1);length--;i--;}}
return data;}
function arrayContains(list,value){var i,length;if(isArray(value)){for(i=0,length=value.length;i<length;i++){if(!arrayContains(list,value[i])){return false;}}
return true;}
var _type=getType(value);for(i=0,length=list.length;i<length;i++){if(_type==='RegExp'){if(typeof list[i]==='string'&&list[i].match(value)){return true;}}else if(list[i]===value){return true;}}
return false;}
function arraysEqual(one,two){if(!isArray(one)||!isArray(two)){return false;}
if(one.length!==two.length){return false;}
one.sort();two.sort();for(var i=0,l=one.length;i<l;i++){if(one[i]!==two[i]){return false;}}
return true;}
function trimSlashes(text){var trim_expression=/^\/+|\/+$/g;return text.replace(trim_expression,'');}
URI._parts=function(){return{protocol:null,username:null,password:null,hostname:null,urn:null,port:null,path:null,query:null,fragment:null,duplicateQueryParameters:URI.duplicateQueryParameters,escapeQuerySpace:URI.escapeQuerySpace};};URI.duplicateQueryParameters=false;URI.escapeQuerySpace=true;URI.protocol_expression=/^[a-z][a-z0-9.+-]*$/i;URI.idn_expression=/[^a-z0-9\.-]/i;URI.punycode_expression=/(xn--)/i;URI.ip4_expression=/^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/;URI.ip6_expression=/^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$/;URI.find_uri_expression=/\b((?:[a-z][\w-]+:(?:\/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}\/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))/ig;URI.findUri={start:/\b(?:([a-z][a-z0-9.+-]*:\/\/)|www\.)/gi,end:/[\s\r\n]|$/,trim:/[`!()\[\]{};:'".,<>?«»“”„‘’]+$/};URI.defaultPorts={http:'80',https:'443',ftp:'21',gopher:'70',ws:'80',wss:'443'};URI.invalid_hostname_characters=/[^a-zA-Z0-9\.-]/;URI.domAttributes={'a':'href','blockquote':'cite','link':'href','base':'href','script':'src','form':'action','img':'src','area':'href','iframe':'src','embed':'src','source':'src','track':'src','input':'src','audio':'src','video':'src'};URI.getDomAttribute=function(node){if(!node||!node.nodeName){return undefined;}
var nodeName=node.nodeName.toLowerCase();if(nodeName==='input'&&node.type!=='image'){return undefined;}
return URI.domAttributes[nodeName];};function escapeForDumbFirefox36(value){return escape(value);}
function strictEncodeURIComponent(string){return encodeURIComponent(string).replace(/[!'()*]/g,escapeForDumbFirefox36).replace(/\*/g,'%2A');}
URI.encode=strictEncodeURIComponent;URI.decode=decodeURIComponent;URI.iso8859=function(){URI.encode=escape;URI.decode=unescape;};URI.unicode=function(){URI.encode=strictEncodeURIComponent;URI.decode=decodeURIComponent;};URI.characters={pathname:{encode:{expression:/%(24|26|2B|2C|3B|3D|3A|40)/ig,map:{'%24':'$','%26':'&','%2B':'+','%2C':',','%3B':';','%3D':'=','%3A':':','%40':'@'}},decode:{expression:/[\/\?#]/g,map:{'/':'%2F','?':'%3F','#':'%23'}}},reserved:{encode:{expression:/%(21|23|24|26|27|28|29|2A|2B|2C|2F|3A|3B|3D|3F|40|5B|5D)/ig,map:{'%3A':':','%2F':'/','%3F':'?','%23':'#','%5B':'[','%5D':']','%40':'@','%21':'!','%24':'$','%26':'&','%27':'\'','%28':'(','%29':')','%2A':'*','%2B':'+','%2C':',','%3B':';','%3D':'='}}},urnpath:{encode:{expression:/%(21|24|27|28|29|2A|2B|2C|3B|3D|40)/ig,map:{'%21':'!','%24':'$','%27':'\'','%28':'(','%29':')','%2A':'*','%2B':'+','%2C':',','%3B':';','%3D':'=','%40':'@'}},decode:{expression:/[\/\?#:]/g,map:{'/':'%2F','?':'%3F','#':'%23',':':'%3A'}}}};URI.encodeQuery=function(string,escapeQuerySpace){var escaped=URI.encode(string+'');if(escapeQuerySpace===undefined){escapeQuerySpace=URI.escapeQuerySpace;}
return escapeQuerySpace?escaped.replace(/%20/g,'+'):escaped;};URI.decodeQuery=function(string,escapeQuerySpace){string+='';if(escapeQuerySpace===undefined){escapeQuerySpace=URI.escapeQuerySpace;}
try{return URI.decode(escapeQuerySpace?string.replace(/\+/g,'%20'):string);}catch(e){return string;}};var _parts={'encode':'encode','decode':'decode'};var _part;var generateAccessor=function(_group,_part){return function(string){try{return URI[_part](string+'').replace(URI.characters[_group][_part].expression,function(c){return URI.characters[_group][_part].map[c];});}catch(e){return string;}};};for(_part in _parts){URI[_part+'PathSegment']=generateAccessor('pathname',_parts[_part]);URI[_part+'UrnPathSegment']=generateAccessor('urnpath',_parts[_part]);}
var generateSegmentedPathFunction=function(_sep,_codingFuncName,_innerCodingFuncName){return function(string){var actualCodingFunc;if(!_innerCodingFuncName){actualCodingFunc=URI[_codingFuncName];}else{actualCodingFunc=function(string){return URI[_codingFuncName](URI[_innerCodingFuncName](string));};}
var segments=(string+'').split(_sep);for(var i=0,length=segments.length;i<length;i++){segments[i]=actualCodingFunc(segments[i]);}
return segments.join(_sep);};};URI.decodePath=generateSegmentedPathFunction('/','decodePathSegment');URI.decodeUrnPath=generateSegmentedPathFunction(':','decodeUrnPathSegment');URI.recodePath=generateSegmentedPathFunction('/','encodePathSegment','decode');URI.recodeUrnPath=generateSegmentedPathFunction(':','encodeUrnPathSegment','decode');URI.encodeReserved=generateAccessor('reserved','encode');URI.parse=function(string,parts){var pos;if(!parts){parts={};}
pos=string.indexOf('#');if(pos>-1){parts.fragment=string.substring(pos+1)||null;string=string.substring(0,pos);}
pos=string.indexOf('?');if(pos>-1){parts.query=string.substring(pos+1)||null;string=string.substring(0,pos);}
if(string.substring(0,2)==='//'){parts.protocol=null;string=string.substring(2);string=URI.parseAuthority(string,parts);}else{pos=string.indexOf(':');if(pos>-1){parts.protocol=string.substring(0,pos)||null;if(parts.protocol&&!parts.protocol.match(URI.protocol_expression)){parts.protocol=undefined;}else if(string.substring(pos+1,pos+3)==='//'){string=string.substring(pos+3);string=URI.parseAuthority(string,parts);}else{string=string.substring(pos+1);parts.urn=true;}}}
parts.path=string;return parts;};URI.parseHost=function(string,parts){string=string.replace(/\\/g,'/');var pos=string.indexOf('/');var bracketPos;var t;if(pos===-1){pos=string.length;}
if(string.charAt(0)==='['){bracketPos=string.indexOf(']');parts.hostname=string.substring(1,bracketPos)||null;parts.port=string.substring(bracketPos+2,pos)||null;if(parts.port==='/'){parts.port=null;}}else{var firstColon=string.indexOf(':');var firstSlash=string.indexOf('/');var nextColon=string.indexOf(':',firstColon+1);if(nextColon!==-1&&(firstSlash===-1||nextColon<firstSlash)){parts.hostname=string.substring(0,pos)||null;parts.port=null;}else{t=string.substring(0,pos).split(':');parts.hostname=t[0]||null;parts.port=t[1]||null;}}
if(parts.hostname&&string.substring(pos).charAt(0)!=='/'){pos++;string='/'+string;}
return string.substring(pos)||'/';};URI.parseAuthority=function(string,parts){string=URI.parseUserinfo(string,parts);return URI.parseHost(string,parts);};URI.parseUserinfo=function(string,parts){var firstSlash=string.indexOf('/');var pos=string.lastIndexOf('@',firstSlash>-1?firstSlash:string.length-1);var t;if(pos>-1&&(firstSlash===-1||pos<firstSlash)){t=string.substring(0,pos).split(':');parts.username=t[0]?URI.decode(t[0]):null;t.shift();parts.password=t[0]?URI.decode(t.join(':')):null;string=string.substring(pos+1);}else{parts.username=null;parts.password=null;}
return string;};URI.parseQuery=function(string,escapeQuerySpace){if(!string){return{};}
string=string.replace(/&+/g,'&').replace(/^\?*&*|&+$/g,'');if(!string){return{};}
var items={};var splits=string.split('&');var length=splits.length;var v,name,value;for(var i=0;i<length;i++){v=splits[i].split('=');name=URI.decodeQuery(v.shift(),escapeQuerySpace);value=v.length?URI.decodeQuery(v.join('='),escapeQuerySpace):null;if(hasOwn.call(items,name)){if(typeof items[name]==='string'||items[name]===null){items[name]=[items[name]];}
items[name].push(value);}else{items[name]=value;}}
return items;};URI.build=function(parts){var t='';if(parts.protocol){t+=parts.protocol+':';}
if(!parts.urn&&(t||parts.hostname)){t+='//';}
t+=(URI.buildAuthority(parts)||'');if(typeof parts.path==='string'){if(parts.path.charAt(0)!=='/'&&typeof parts.hostname==='string'){t+='/';}
t+=parts.path;}
if(typeof parts.query==='string'&&parts.query){t+='?'+parts.query;}
if(typeof parts.fragment==='string'&&parts.fragment){t+='#'+parts.fragment;}
return t;};URI.buildHost=function(parts){var t='';if(!parts.hostname){return'';}else if(URI.ip6_expression.test(parts.hostname)){t+='['+parts.hostname+']';}else{t+=parts.hostname;}
if(parts.port){t+=':'+parts.port;}
return t;};URI.buildAuthority=function(parts){return URI.buildUserinfo(parts)+URI.buildHost(parts);};URI.buildUserinfo=function(parts){var t='';if(parts.username){t+=URI.encode(parts.username);if(parts.password){t+=':'+URI.encode(parts.password);}
t+='@';}
return t;};URI.buildQuery=function(data,duplicateQueryParameters,escapeQuerySpace){var t='';var unique,key,i,length;for(key in data){if(hasOwn.call(data,key)&&key){if(isArray(data[key])){unique={};for(i=0,length=data[key].length;i<length;i++){if(data[key][i]!==undefined&&unique[data[key][i]+'']===undefined){t+='&'+URI.buildQueryParameter(key,data[key][i],escapeQuerySpace);if(duplicateQueryParameters!==true){unique[data[key][i]+'']=true;}}}}else if(data[key]!==undefined){t+='&'+URI.buildQueryParameter(key,data[key],escapeQuerySpace);}}}
return t.substring(1);};URI.buildQueryParameter=function(name,value,escapeQuerySpace){return URI.encodeQuery(name,escapeQuerySpace)+(value!==null?'='+URI.encodeQuery(value,escapeQuerySpace):'');};URI.addQuery=function(data,name,value){if(typeof name==='object'){for(var key in name){if(hasOwn.call(name,key)){URI.addQuery(data,key,name[key]);}}}else if(typeof name==='string'){if(data[name]===undefined){data[name]=value;return;}else if(typeof data[name]==='string'){data[name]=[data[name]];}
if(!isArray(value)){value=[value];}
data[name]=(data[name]||[]).concat(value);}else{throw new TypeError('URI.addQuery() accepts an object, string as the name parameter');}};URI.removeQuery=function(data,name,value){var i,length,key;if(isArray(name)){for(i=0,length=name.length;i<length;i++){data[name[i]]=undefined;}}else if(getType(name)==='RegExp'){for(key in data){if(name.test(key)){data[key]=undefined;}}}else if(typeof name==='object'){for(key in name){if(hasOwn.call(name,key)){URI.removeQuery(data,key,name[key]);}}}else if(typeof name==='string'){if(value!==undefined){if(getType(value)==='RegExp'){if(!isArray(data[name])&&value.test(data[name])){data[name]=undefined;}else{data[name]=filterArrayValues(data[name],value);}}else if(data[name]===String(value)&&(!isArray(value)||value.length===1)){data[name]=undefined;}else if(isArray(data[name])){data[name]=filterArrayValues(data[name],value);}}else{data[name]=undefined;}}else{throw new TypeError('URI.removeQuery() accepts an object, string, RegExp as the first parameter');}};URI.hasQuery=function(data,name,value,withinArray){switch(getType(name)){case'String':break;case'RegExp':for(var key in data){if(hasOwn.call(data,key)){if(name.test(key)&&(value===undefined||URI.hasQuery(data,key,value))){return true;}}}
return false;case'Object':for(var _key in name){if(hasOwn.call(name,_key)){if(!URI.hasQuery(data,_key,name[_key])){return false;}}}
return true;default:throw new TypeError('URI.hasQuery() accepts a string, regular expression or object as the name parameter');}
switch(getType(value)){case'Undefined':return name in data;case'Boolean':var _booly=Boolean(isArray(data[name])?data[name].length:data[name]);return value===_booly;case'Function':return!!value(data[name],name,data);case'Array':if(!isArray(data[name])){return false;}
var op=withinArray?arrayContains:arraysEqual;return op(data[name],value);case'RegExp':if(!isArray(data[name])){return Boolean(data[name]&&data[name].match(value));}
if(!withinArray){return false;}
return arrayContains(data[name],value);case'Number':value=String(value);case'String':if(!isArray(data[name])){return data[name]===value;}
if(!withinArray){return false;}
return arrayContains(data[name],value);default:throw new TypeError('URI.hasQuery() accepts undefined, boolean, string, number, RegExp, Function as the value parameter');}};URI.commonPath=function(one,two){var length=Math.min(one.length,two.length);var pos;for(pos=0;pos<length;pos++){if(one.charAt(pos)!==two.charAt(pos)){pos--;break;}}
if(pos<1){return one.charAt(0)===two.charAt(0)&&one.charAt(0)==='/'?'/':'';}
if(one.charAt(pos)!=='/'||two.charAt(pos)!=='/'){pos=one.substring(0,pos).lastIndexOf('/');}
return one.substring(0,pos+1);};URI.withinString=function(string,callback,options){options||(options={});var _start=options.start||URI.findUri.start;var _end=options.end||URI.findUri.end;var _trim=options.trim||URI.findUri.trim;var _attributeOpen=/[a-z0-9-]=["']?$/i;_start.lastIndex=0;while(true){var match=_start.exec(string);if(!match){break;}
var start=match.index;if(options.ignoreHtml){var attributeOpen=string.slice(Math.max(start-3,0),start);if(attributeOpen&&_attributeOpen.test(attributeOpen)){continue;}}
var end=start+string.slice(start).search(_end);var slice=string.slice(start,end).replace(_trim,'');if(options.ignore&&options.ignore.test(slice)){continue;}
end=start+slice.length;var result=callback(slice,start,end,string);string=string.slice(0,start)+result+string.slice(end);_start.lastIndex=start+result.length;}
_start.lastIndex=0;return string;};URI.ensureValidHostname=function(v){if(v.match(URI.invalid_hostname_characters)){if(!punycode){throw new TypeError('Hostname "'+v+'" contains characters other than [A-Z0-9.-] and Punycode.js is not available');}
if(punycode.toASCII(v).match(URI.invalid_hostname_characters)){throw new TypeError('Hostname "'+v+'" contains characters other than [A-Z0-9.-]');}}};URI.noConflict=function(removeAll){if(removeAll){var unconflicted={URI:this.noConflict()};if(root.URITemplate&&typeof root.URITemplate.noConflict==='function'){unconflicted.URITemplate=root.URITemplate.noConflict();}
if(root.IPv6&&typeof root.IPv6.noConflict==='function'){unconflicted.IPv6=root.IPv6.noConflict();}
if(root.SecondLevelDomains&&typeof root.SecondLevelDomains.noConflict==='function'){unconflicted.SecondLevelDomains=root.SecondLevelDomains.noConflict();}
return unconflicted;}else if(root.URI===this){root.URI=_URI;}
return this;};p.build=function(deferBuild){if(deferBuild===true){this._deferred_build=true;}else if(deferBuild===undefined||this._deferred_build){this._string=URI.build(this._parts);this._deferred_build=false;}
return this;};p.clone=function(){return new URI(this);};p.valueOf=p.toString=function(){return this.build(false)._string;};function generateSimpleAccessor(_part){return function(v,build){if(v===undefined){return this._parts[_part]||'';}else{this._parts[_part]=v||null;this.build(!build);return this;}};}
function generatePrefixAccessor(_part,_key){return function(v,build){if(v===undefined){return this._parts[_part]||'';}else{if(v!==null){v=v+'';if(v.charAt(0)===_key){v=v.substring(1);}}
this._parts[_part]=v;this.build(!build);return this;}};}
p.protocol=generateSimpleAccessor('protocol');p.username=generateSimpleAccessor('username');p.password=generateSimpleAccessor('password');p.hostname=generateSimpleAccessor('hostname');p.port=generateSimpleAccessor('port');p.query=generatePrefixAccessor('query','?');p.fragment=generatePrefixAccessor('fragment','#');p.search=function(v,build){var t=this.query(v,build);return typeof t==='string'&&t.length?('?'+t):t;};p.hash=function(v,build){var t=this.fragment(v,build);return typeof t==='string'&&t.length?('#'+t):t;};p.pathname=function(v,build){if(v===undefined||v===true){var res=this._parts.path||(this._parts.hostname?'/':'');return v?(this._parts.urn?URI.decodeUrnPath:URI.decodePath)(res):res;}else{if(this._parts.urn){this._parts.path=v?URI.recodeUrnPath(v):'';}else{this._parts.path=v?URI.recodePath(v):'/';}
this.build(!build);return this;}};p.path=p.pathname;p.href=function(href,build){var key;if(href===undefined){return this.toString();}
this._string='';this._parts=URI._parts();var _URI=href instanceof URI;var _object=typeof href==='object'&&(href.hostname||href.path||href.pathname);if(href.nodeName){var attribute=URI.getDomAttribute(href);href=href[attribute]||'';_object=false;}
if(!_URI&&_object&&href.pathname!==undefined){href=href.toString();}
if(typeof href==='string'||href instanceof String){this._parts=URI.parse(String(href),this._parts);}else if(_URI||_object){var src=_URI?href._parts:href;for(key in src){if(hasOwn.call(this._parts,key)){this._parts[key]=src[key];}}}else{throw new TypeError('invalid input');}
this.build(!build);return this;};p.is=function(what){var ip=false;var ip4=false;var ip6=false;var name=false;var sld=false;var idn=false;var punycode=false;var relative=!this._parts.urn;if(this._parts.hostname){relative=false;ip4=URI.ip4_expression.test(this._parts.hostname);ip6=URI.ip6_expression.test(this._parts.hostname);ip=ip4||ip6;name=!ip;sld=name&&SLD&&SLD.has(this._parts.hostname);idn=name&&URI.idn_expression.test(this._parts.hostname);punycode=name&&URI.punycode_expression.test(this._parts.hostname);}
switch(what.toLowerCase()){case'relative':return relative;case'absolute':return!relative;case'domain':case'name':return name;case'sld':return sld;case'ip':return ip;case'ip4':case'ipv4':case'inet4':return ip4;case'ip6':case'ipv6':case'inet6':return ip6;case'idn':return idn;case'url':return!this._parts.urn;case'urn':return!!this._parts.urn;case'punycode':return punycode;}
return null;};var _protocol=p.protocol;var _port=p.port;var _hostname=p.hostname;p.protocol=function(v,build){if(v!==undefined){if(v){v=v.replace(/:(\/\/)?$/,'');if(!v.match(URI.protocol_expression)){throw new TypeError('Protocol "'+v+'" contains characters other than [A-Z0-9.+-] or doesn\'t start with [A-Z]');}}}
return _protocol.call(this,v,build);};p.scheme=p.protocol;p.port=function(v,build){if(this._parts.urn){return v===undefined?'':this;}
if(v!==undefined){if(v===0){v=null;}
if(v){v+='';if(v.charAt(0)===':'){v=v.substring(1);}
if(v.match(/[^0-9]/)){throw new TypeError('Port "'+v+'" contains characters other than [0-9]');}}}
return _port.call(this,v,build);};p.hostname=function(v,build){if(this._parts.urn){return v===undefined?'':this;}
if(v!==undefined){var x={};var res=URI.parseHost(v,x);if(res!=='/'){throw new TypeError('Hostname "'+v+'" contains characters other than [A-Z0-9.-]');}
v=x.hostname;}
return _hostname.call(this,v,build);};p.origin=function(v,build){if(this._parts.urn){return v===undefined?'':this;}
if(v===undefined){var protocol=this.protocol();var authority=this.authority();if(!authority){return'';}
return(protocol?protocol+'://':'')+this.authority();}else{var origin=URI(v);this.protocol(origin.protocol()).authority(origin.authority()).build(!build);return this;}};p.host=function(v,build){if(this._parts.urn){return v===undefined?'':this;}
if(v===undefined){return this._parts.hostname?URI.buildHost(this._parts):'';}else{var res=URI.parseHost(v,this._parts);if(res!=='/'){throw new TypeError('Hostname "'+v+'" contains characters other than [A-Z0-9.-]');}
this.build(!build);return this;}};p.authority=function(v,build){if(this._parts.urn){return v===undefined?'':this;}
if(v===undefined){return this._parts.hostname?URI.buildAuthority(this._parts):'';}else{var res=URI.parseAuthority(v,this._parts);if(res!=='/'){throw new TypeError('Hostname "'+v+'" contains characters other than [A-Z0-9.-]');}
this.build(!build);return this;}};p.userinfo=function(v,build){if(this._parts.urn){return v===undefined?'':this;}
if(v===undefined){if(!this._parts.username){return'';}
var t=URI.buildUserinfo(this._parts);return t.substring(0,t.length-1);}else{if(v[v.length-1]!=='@'){v+='@';}
URI.parseUserinfo(v,this._parts);this.build(!build);return this;}};p.resource=function(v,build){var parts;if(v===undefined){return this.path()+this.search()+this.hash();}
parts=URI.parse(v);this._parts.path=parts.path;this._parts.query=parts.query;this._parts.fragment=parts.fragment;this.build(!build);return this;};p.subdomain=function(v,build){if(this._parts.urn){return v===undefined?'':this;}
if(v===undefined){if(!this._parts.hostname||this.is('IP')){return'';}
var end=this._parts.hostname.length-this.domain().length-1;return this._parts.hostname.substring(0,end)||'';}else{var e=this._parts.hostname.length-this.domain().length;var sub=this._parts.hostname.substring(0,e);var replace=new RegExp('^'+escapeRegEx(sub));if(v&&v.charAt(v.length-1)!=='.'){v+='.';}
if(v){URI.ensureValidHostname(v);}
this._parts.hostname=this._parts.hostname.replace(replace,v);this.build(!build);return this;}};p.domain=function(v,build){if(this._parts.urn){return v===undefined?'':this;}
if(typeof v==='boolean'){build=v;v=undefined;}
if(v===undefined){if(!this._parts.hostname||this.is('IP')){return'';}
var t=this._parts.hostname.match(/\./g);if(t&&t.length<2){return this._parts.hostname;}
var end=this._parts.hostname.length-this.tld(build).length-1;end=this._parts.hostname.lastIndexOf('.',end-1)+1;return this._parts.hostname.substring(end)||'';}else{if(!v){throw new TypeError('cannot set domain empty');}
URI.ensureValidHostname(v);if(!this._parts.hostname||this.is('IP')){this._parts.hostname=v;}else{var replace=new RegExp(escapeRegEx(this.domain())+'$');this._parts.hostname=this._parts.hostname.replace(replace,v);}
this.build(!build);return this;}};p.tld=function(v,build){if(this._parts.urn){return v===undefined?'':this;}
if(typeof v==='boolean'){build=v;v=undefined;}
if(v===undefined){if(!this._parts.hostname||this.is('IP')){return'';}
var pos=this._parts.hostname.lastIndexOf('.');var tld=this._parts.hostname.substring(pos+1);if(build!==true&&SLD&&SLD.list[tld.toLowerCase()]){return SLD.get(this._parts.hostname)||tld;}
return tld;}else{var replace;if(!v){throw new TypeError('cannot set TLD empty');}else if(v.match(/[^a-zA-Z0-9-]/)){if(SLD&&SLD.is(v)){replace=new RegExp(escapeRegEx(this.tld())+'$');this._parts.hostname=this._parts.hostname.replace(replace,v);}else{throw new TypeError('TLD "'+v+'" contains characters other than [A-Z0-9]');}}else if(!this._parts.hostname||this.is('IP')){throw new ReferenceError('cannot set TLD on non-domain host');}else{replace=new RegExp(escapeRegEx(this.tld())+'$');this._parts.hostname=this._parts.hostname.replace(replace,v);}
this.build(!build);return this;}};p.directory=function(v,build){if(this._parts.urn){return v===undefined?'':this;}
if(v===undefined||v===true){if(!this._parts.path&&!this._parts.hostname){return'';}
if(this._parts.path==='/'){return'/';}
var end=this._parts.path.length-this.filename().length-1;var res=this._parts.path.substring(0,end)||(this._parts.hostname?'/':'');return v?URI.decodePath(res):res;}else{var e=this._parts.path.length-this.filename().length;var directory=this._parts.path.substring(0,e);var replace=new RegExp('^'+escapeRegEx(directory));if(!this.is('relative')){if(!v){v='/';}
if(v.charAt(0)!=='/'){v='/'+v;}}
if(v&&v.charAt(v.length-1)!=='/'){v+='/';}
v=URI.recodePath(v);this._parts.path=this._parts.path.replace(replace,v);this.build(!build);return this;}};p.filename=function(v,build){if(this._parts.urn){return v===undefined?'':this;}
if(v===undefined||v===true){if(!this._parts.path||this._parts.path==='/'){return'';}
var pos=this._parts.path.lastIndexOf('/');var res=this._parts.path.substring(pos+1);return v?URI.decodePathSegment(res):res;}else{var mutatedDirectory=false;if(v.charAt(0)==='/'){v=v.substring(1);}
if(v.match(/\.?\//)){mutatedDirectory=true;}
var replace=new RegExp(escapeRegEx(this.filename())+'$');v=URI.recodePath(v);this._parts.path=this._parts.path.replace(replace,v);if(mutatedDirectory){this.normalizePath(build);}else{this.build(!build);}
return this;}};p.suffix=function(v,build){if(this._parts.urn){return v===undefined?'':this;}
if(v===undefined||v===true){if(!this._parts.path||this._parts.path==='/'){return'';}
var filename=this.filename();var pos=filename.lastIndexOf('.');var s,res;if(pos===-1){return'';}
s=filename.substring(pos+1);res=(/^[a-z0-9%]+$/i).test(s)?s:'';return v?URI.decodePathSegment(res):res;}else{if(v.charAt(0)==='.'){v=v.substring(1);}
var suffix=this.suffix();var replace;if(!suffix){if(!v){return this;}
this._parts.path+='.'+URI.recodePath(v);}else if(!v){replace=new RegExp(escapeRegEx('.'+suffix)+'$');}else{replace=new RegExp(escapeRegEx(suffix)+'$');}
if(replace){v=URI.recodePath(v);this._parts.path=this._parts.path.replace(replace,v);}
this.build(!build);return this;}};p.segment=function(segment,v,build){var separator=this._parts.urn?':':'/';var path=this.path();var absolute=path.substring(0,1)==='/';var segments=path.split(separator);if(segment!==undefined&&typeof segment!=='number'){build=v;v=segment;segment=undefined;}
if(segment!==undefined&&typeof segment!=='number'){throw new Error('Bad segment "'+segment+'", must be 0-based integer');}
if(absolute){segments.shift();}
if(segment<0){segment=Math.max(segments.length+segment,0);}
if(v===undefined){return segment===undefined?segments:segments[segment];}else if(segment===null||segments[segment]===undefined){if(isArray(v)){segments=[];for(var i=0,l=v.length;i<l;i++){if(!v[i].length&&(!segments.length||!segments[segments.length-1].length)){continue;}
if(segments.length&&!segments[segments.length-1].length){segments.pop();}
segments.push(trimSlashes(v[i]));}}else if(v||typeof v==='string'){v=trimSlashes(v);if(segments[segments.length-1]===''){segments[segments.length-1]=v;}else{segments.push(v);}}}else{if(v){segments[segment]=trimSlashes(v);}else{segments.splice(segment,1);}}
if(absolute){segments.unshift('');}
return this.path(segments.join(separator),build);};p.segmentCoded=function(segment,v,build){var segments,i,l;if(typeof segment!=='number'){build=v;v=segment;segment=undefined;}
if(v===undefined){segments=this.segment(segment,v,build);if(!isArray(segments)){segments=segments!==undefined?URI.decode(segments):undefined;}else{for(i=0,l=segments.length;i<l;i++){segments[i]=URI.decode(segments[i]);}}
return segments;}
if(!isArray(v)){v=(typeof v==='string'||v instanceof String)?URI.encode(v):v;}else{for(i=0,l=v.length;i<l;i++){v[i]=URI.encode(v[i]);}}
return this.segment(segment,v,build);};var q=p.query;p.query=function(v,build){if(v===true){return URI.parseQuery(this._parts.query,this._parts.escapeQuerySpace);}else if(typeof v==='function'){var data=URI.parseQuery(this._parts.query,this._parts.escapeQuerySpace);var result=v.call(this,data);this._parts.query=URI.buildQuery(result||data,this._parts.duplicateQueryParameters,this._parts.escapeQuerySpace);this.build(!build);return this;}else if(v!==undefined&&typeof v!=='string'){this._parts.query=URI.buildQuery(v,this._parts.duplicateQueryParameters,this._parts.escapeQuerySpace);this.build(!build);return this;}else{return q.call(this,v,build);}};p.setQuery=function(name,value,build){var data=URI.parseQuery(this._parts.query,this._parts.escapeQuerySpace);if(typeof name==='string'||name instanceof String){data[name]=value!==undefined?value:null;}else if(typeof name==='object'){for(var key in name){if(hasOwn.call(name,key)){data[key]=name[key];}}}else{throw new TypeError('URI.addQuery() accepts an object, string as the name parameter');}
this._parts.query=URI.buildQuery(data,this._parts.duplicateQueryParameters,this._parts.escapeQuerySpace);if(typeof name!=='string'){build=value;}
this.build(!build);return this;};p.addQuery=function(name,value,build){var data=URI.parseQuery(this._parts.query,this._parts.escapeQuerySpace);URI.addQuery(data,name,value===undefined?null:value);this._parts.query=URI.buildQuery(data,this._parts.duplicateQueryParameters,this._parts.escapeQuerySpace);if(typeof name!=='string'){build=value;}
this.build(!build);return this;};p.removeQuery=function(name,value,build){var data=URI.parseQuery(this._parts.query,this._parts.escapeQuerySpace);URI.removeQuery(data,name,value);this._parts.query=URI.buildQuery(data,this._parts.duplicateQueryParameters,this._parts.escapeQuerySpace);if(typeof name!=='string'){build=value;}
this.build(!build);return this;};p.hasQuery=function(name,value,withinArray){var data=URI.parseQuery(this._parts.query,this._parts.escapeQuerySpace);return URI.hasQuery(data,name,value,withinArray);};p.setSearch=p.setQuery;p.addSearch=p.addQuery;p.removeSearch=p.removeQuery;p.hasSearch=p.hasQuery;p.normalize=function(){if(this._parts.urn){return this.normalizeProtocol(false).normalizePath(false).normalizeQuery(false).normalizeFragment(false).build();}
return this.normalizeProtocol(false).normalizeHostname(false).normalizePort(false).normalizePath(false).normalizeQuery(false).normalizeFragment(false).build();};p.normalizeProtocol=function(build){if(typeof this._parts.protocol==='string'){this._parts.protocol=this._parts.protocol.toLowerCase();this.build(!build);}
return this;};p.normalizeHostname=function(build){if(this._parts.hostname){if(this.is('IDN')&&punycode){this._parts.hostname=punycode.toASCII(this._parts.hostname);}else if(this.is('IPv6')&&IPv6){this._parts.hostname=IPv6.best(this._parts.hostname);}
this._parts.hostname=this._parts.hostname.toLowerCase();this.build(!build);}
return this;};p.normalizePort=function(build){if(typeof this._parts.protocol==='string'&&this._parts.port===URI.defaultPorts[this._parts.protocol]){this._parts.port=null;this.build(!build);}
return this;};p.normalizePath=function(build){var _path=this._parts.path;if(!_path){return this;}
if(this._parts.urn){this._parts.path=URI.recodeUrnPath(this._parts.path);this.build(!build);return this;}
if(this._parts.path==='/'){return this;}
_path=URI.recodePath(_path);var _was_relative;var _leadingParents='';var _parent,_pos;if(_path.charAt(0)!=='/'){_was_relative=true;_path='/'+_path;}
if(_path.slice(-3)==='/..'||_path.slice(-2)==='/.'){_path+='/';}
_path=_path.replace(/(\/(\.\/)+)|(\/\.$)/g,'/').replace(/\/{2,}/g,'/');if(_was_relative){_leadingParents=_path.substring(1).match(/^(\.\.\/)+/)||'';if(_leadingParents){_leadingParents=_leadingParents[0];}}
while(true){_parent=_path.search(/\/\.\.(\/|$)/);if(_parent===-1){break;}else if(_parent===0){_path=_path.substring(3);continue;}
_pos=_path.substring(0,_parent).lastIndexOf('/');if(_pos===-1){_pos=_parent;}
_path=_path.substring(0,_pos)+_path.substring(_parent+3);}
if(_was_relative&&this.is('relative')){_path=_leadingParents+_path.substring(1);}
this._parts.path=_path;this.build(!build);return this;};p.normalizePathname=p.normalizePath;p.normalizeQuery=function(build){if(typeof this._parts.query==='string'){if(!this._parts.query.length){this._parts.query=null;}else{this.query(URI.parseQuery(this._parts.query,this._parts.escapeQuerySpace));}
this.build(!build);}
return this;};p.normalizeFragment=function(build){if(!this._parts.fragment){this._parts.fragment=null;this.build(!build);}
return this;};p.normalizeSearch=p.normalizeQuery;p.normalizeHash=p.normalizeFragment;p.iso8859=function(){var e=URI.encode;var d=URI.decode;URI.encode=escape;URI.decode=decodeURIComponent;try{this.normalize();}finally{URI.encode=e;URI.decode=d;}
return this;};p.unicode=function(){var e=URI.encode;var d=URI.decode;URI.encode=strictEncodeURIComponent;URI.decode=unescape;try{this.normalize();}finally{URI.encode=e;URI.decode=d;}
return this;};p.readable=function(){var uri=this.clone();uri.username('').password('').normalize();var t='';if(uri._parts.protocol){t+=uri._parts.protocol+'://';}
if(uri._parts.hostname){if(uri.is('punycode')&&punycode){t+=punycode.toUnicode(uri._parts.hostname);if(uri._parts.port){t+=':'+uri._parts.port;}}else{t+=uri.host();}}
if(uri._parts.hostname&&uri._parts.path&&uri._parts.path.charAt(0)!=='/'){t+='/';}
t+=uri.path(true);if(uri._parts.query){var q='';for(var i=0,qp=uri._parts.query.split('&'),l=qp.length;i<l;i++){var kv=(qp[i]||'').split('=');q+='&'+URI.decodeQuery(kv[0],this._parts.escapeQuerySpace).replace(/&/g,'%26');if(kv[1]!==undefined){q+='='+URI.decodeQuery(kv[1],this._parts.escapeQuerySpace).replace(/&/g,'%26');}}
t+='?'+q.substring(1);}
t+=URI.decodeQuery(uri.hash(),true);return t;};p.absoluteTo=function(base){var resolved=this.clone();var properties=['protocol','username','password','hostname','port'];var basedir,i,p;if(this._parts.urn){throw new Error('URNs do not have any generally defined hierarchical components');}
if(!(base instanceof URI)){base=new URI(base);}
if(!resolved._parts.protocol){resolved._parts.protocol=base._parts.protocol;}
if(this._parts.hostname){return resolved;}
for(i=0;(p=properties[i]);i++){resolved._parts[p]=base._parts[p];}
if(!resolved._parts.path){resolved._parts.path=base._parts.path;if(!resolved._parts.query){resolved._parts.query=base._parts.query;}}else if(resolved._parts.path.substring(-2)==='..'){resolved._parts.path+='/';}
if(resolved.path().charAt(0)!=='/'){basedir=base.directory();basedir=basedir?basedir:base.path().indexOf('/')===0?'/':'';resolved._parts.path=(basedir?(basedir+'/'):'')+resolved._parts.path;resolved.normalizePath();}
resolved.build();return resolved;};p.relativeTo=function(base){var relative=this.clone().normalize();var relativeParts,baseParts,common,relativePath,basePath;if(relative._parts.urn){throw new Error('URNs do not have any generally defined hierarchical components');}
base=new URI(base).normalize();relativeParts=relative._parts;baseParts=base._parts;relativePath=relative.path();basePath=base.path();if(relativePath.charAt(0)!=='/'){throw new Error('URI is already relative');}
if(basePath.charAt(0)!=='/'){throw new Error('Cannot calculate a URI relative to another relative URI');}
if(relativeParts.protocol===baseParts.protocol){relativeParts.protocol=null;}
if(relativeParts.username!==baseParts.username||relativeParts.password!==baseParts.password){return relative.build();}
if(relativeParts.protocol!==null||relativeParts.username!==null||relativeParts.password!==null){return relative.build();}
if(relativeParts.hostname===baseParts.hostname&&relativeParts.port===baseParts.port){relativeParts.hostname=null;relativeParts.port=null;}else{return relative.build();}
if(relativePath===basePath){relativeParts.path='';return relative.build();}
common=URI.commonPath(relativePath,basePath);if(!common){return relative.build();}
var parents=baseParts.path.substring(common.length).replace(/[^\/]*$/,'').replace(/.*?\//g,'../');relativeParts.path=(parents+relativeParts.path.substring(common.length))||'./';return relative.build();};p.equals=function(uri){var one=this.clone();var two=new URI(uri);var one_map={};var two_map={};var checked={};var one_query,two_query,key;one.normalize();two.normalize();if(one.toString()===two.toString()){return true;}
one_query=one.query();two_query=two.query();one.query('');two.query('');if(one.toString()!==two.toString()){return false;}
if(one_query.length!==two_query.length){return false;}
one_map=URI.parseQuery(one_query,this._parts.escapeQuerySpace);two_map=URI.parseQuery(two_query,this._parts.escapeQuerySpace);for(key in one_map){if(hasOwn.call(one_map,key)){if(!isArray(one_map[key])){if(one_map[key]!==two_map[key]){return false;}}else if(!arraysEqual(one_map[key],two_map[key])){return false;}
checked[key]=true;}}
for(key in two_map){if(hasOwn.call(two_map,key)){if(!checked[key]){return false;}}}
return true;};p.duplicateQueryParameters=function(v){this._parts.duplicateQueryParameters=!!v;return this;};p.escapeQuerySpace=function(v){this._parts.escapeQuerySpace=!!v;return this;};return URI;}));(function(global,$){"use strict";if(global.URI){global.URI.prototype.getSearch=function(name,defaultValue){var searchValues=this.search(true);if(searchValues.hasOwnProperty(name)){return searchValues[name];}
return defaultValue;};}}(typeof window!=='undefined'?window:this,jQuery));;(function(){"use strict";function setup($){$.fn._fadeIn=$.fn.fadeIn;var noOp=$.noop||function(){};var msie=/MSIE/.test(navigator.userAgent);var ie6=/MSIE 6.0/.test(navigator.userAgent)&&!/MSIE 8.0/.test(navigator.userAgent);var mode=document.documentMode||0;var setExpr=$.isFunction(document.createElement('div').style.setExpression);$.blockUI=function(opts){install(window,opts);};$.unblockUI=function(opts){remove(window,opts);};$.growlUI=function(title,message,timeout,onClose){var $m=$('<div class="growlUI"></div>');if(title)$m.append('<h1>'+title+'</h1>');if(message)$m.append('<h2>'+message+'</h2>');if(timeout===undefined)timeout=3000;var callBlock=function(opts){opts=opts||{};$.blockUI({message:$m,fadeIn:typeof opts.fadeIn!=='undefined'?opts.fadeIn:700,fadeOut:typeof opts.fadeOut!=='undefined'?opts.fadeOut:1000,timeout:typeof opts.timeout!=='undefined'?opts.timeout:timeout,centerY:false,showOverlay:false,onUnblock:onClose,css:$.blockUI.defaults.growlCSS});};callBlock();var nonmousedOpacity=$m.css('opacity');$m.mouseover(function(){callBlock({fadeIn:0,timeout:30000});var displayBlock=$('.blockMsg');displayBlock.stop();displayBlock.fadeTo(300,1);}).mouseout(function(){$('.blockMsg').fadeOut(1000);});};$.fn.block=function(opts){if(this[0]===window){$.blockUI(opts);return this;}
var fullOpts=$.extend({},$.blockUI.defaults,opts||{});this.each(function(){var $el=$(this);if(fullOpts.ignoreIfBlocked&&$el.data('blockUI.isBlocked'))
return;$el.unblock({fadeOut:0});});return this.each(function(){if($.css(this,'position')=='static'){this.style.position='relative';$(this).data('blockUI.static',true);}
this.style.zoom=1;install(this,opts);});};$.fn.unblock=function(opts){if(this[0]===window){$.unblockUI(opts);return this;}
return this.each(function(){remove(this,opts);});};$.blockUI.version=2.70;$.blockUI.defaults={message:'<h1>Please wait...</h1>',title:null,draggable:true,theme:false,css:{padding:0,margin:0,width:'30%',top:'40%',left:'35%',textAlign:'center',color:'#000',border:'3px solid #aaa',backgroundColor:'#fff',cursor:'wait'},themedCSS:{width:'30%',top:'40%',left:'35%'},overlayCSS:{backgroundColor:'#000',opacity:0.6,cursor:'wait'},cursorReset:'default',growlCSS:{width:'350px',top:'10px',left:'',right:'10px',border:'none',padding:'5px',opacity:0.6,cursor:'default',color:'#fff',backgroundColor:'#000','-webkit-border-radius':'10px','-moz-border-radius':'10px','border-radius':'10px'},iframeSrc:/^https/i.test(window.location.href||'')?'javascript:false':'about:blank',forceIframe:false,baseZ:1000,centerX:true,centerY:true,allowBodyStretch:true,bindEvents:true,constrainTabKey:true,fadeIn:200,fadeOut:400,timeout:0,showOverlay:true,focusInput:true,focusableElements:':input:enabled:visible',onBlock:null,onUnblock:null,onOverlayClick:null,quirksmodeOffsetHack:4,blockMsgClass:'blockMsg',ignoreIfBlocked:false};var pageBlock=null;var pageBlockEls=[];function install(el,opts){var css,themedCSS;var full=(el==window);var msg=(opts&&opts.message!==undefined?opts.message:undefined);opts=$.extend({},$.blockUI.defaults,opts||{});if(opts.ignoreIfBlocked&&$(el).data('blockUI.isBlocked'))
return;opts.overlayCSS=$.extend({},$.blockUI.defaults.overlayCSS,opts.overlayCSS||{});css=$.extend({},$.blockUI.defaults.css,opts.css||{});if(opts.onOverlayClick)
opts.overlayCSS.cursor='pointer';themedCSS=$.extend({},$.blockUI.defaults.themedCSS,opts.themedCSS||{});msg=msg===undefined?opts.message:msg;if(full&&pageBlock)
remove(window,{fadeOut:0});if(msg&&typeof msg!='string'&&(msg.parentNode||msg.jquery)){var node=msg.jquery?msg[0]:msg;var data={};$(el).data('blockUI.history',data);data.el=node;data.parent=node.parentNode;data.display=node.style.display;data.position=node.style.position;if(data.parent)
data.parent.removeChild(node);}
$(el).data('blockUI.onUnblock',opts.onUnblock);var z=opts.baseZ;var lyr1,lyr2,lyr3,s;if(msie||opts.forceIframe)
lyr1=$('<iframe class="blockUI" style="z-index:'+(z++)+';display:none;border:none;margin:0;padding:0;position:absolute;width:100%;height:100%;top:0;left:0" src="'+opts.iframeSrc+'"></iframe>');else
lyr1=$('<div class="blockUI" style="display:none"></div>');if(opts.theme)
lyr2=$('<div class="blockUI blockOverlay ui-widget-overlay" style="z-index:'+(z++)+';display:none"></div>');else
lyr2=$('<div class="blockUI blockOverlay" style="z-index:'+(z++)+';display:none;border:none;margin:0;padding:0;width:100%;height:100%;top:0;left:0"></div>');if(opts.theme&&full){s='<div class="blockUI '+opts.blockMsgClass+' blockPage ui-dialog ui-widget ui-corner-all" style="z-index:'+(z+10)+';display:none;position:fixed">';if(opts.title){s+='<div class="ui-widget-header ui-dialog-titlebar ui-corner-all blockTitle">'+(opts.title||'&nbsp;')+'</div>';}
s+='<div class="ui-widget-content ui-dialog-content"></div>';s+='</div>';}
else if(opts.theme){s='<div class="blockUI '+opts.blockMsgClass+' blockElement ui-dialog ui-widget ui-corner-all" style="z-index:'+(z+10)+';display:none;position:absolute">';if(opts.title){s+='<div class="ui-widget-header ui-dialog-titlebar ui-corner-all blockTitle">'+(opts.title||'&nbsp;')+'</div>';}
s+='<div class="ui-widget-content ui-dialog-content"></div>';s+='</div>';}
else if(full){s='<div class="blockUI '+opts.blockMsgClass+' blockPage" style="z-index:'+(z+10)+';display:none;position:fixed"></div>';}
else{s='<div class="blockUI '+opts.blockMsgClass+' blockElement" style="z-index:'+(z+10)+';display:none;position:absolute"></div>';}
lyr3=$(s);if(msg){if(opts.theme){lyr3.css(themedCSS);lyr3.addClass('ui-widget-content');}
else
lyr3.css(css);}
if(!opts.theme)
lyr2.css(opts.overlayCSS);lyr2.css('position',full?'fixed':'absolute');if(msie||opts.forceIframe)
lyr1.css('opacity',0.0);var layers=[lyr1,lyr2,lyr3],$par=full?$('body'):$(el);$.each(layers,function(){this.appendTo($par);});if(opts.theme&&opts.draggable&&$.fn.draggable){lyr3.draggable({handle:'.ui-dialog-titlebar',cancel:'li'});}
var expr=setExpr&&(!$.support.boxModel||$('object,embed',full?null:el).length>0);if(ie6||expr){if(full&&opts.allowBodyStretch&&$.support.boxModel)
$('html,body').css('height','100%');if((ie6||!$.support.boxModel)&&!full){var t=sz(el,'borderTopWidth'),l=sz(el,'borderLeftWidth');var fixT=t?'(0 - '+t+')':0;var fixL=l?'(0 - '+l+')':0;}
$.each(layers,function(i,o){var s=o[0].style;s.position='absolute';if(i<2){if(full)
s.setExpression('height','Math.max(document.body.scrollHeight, document.body.offsetHeight) - (jQuery.support.boxModel?0:'+opts.quirksmodeOffsetHack+') + "px"');else
s.setExpression('height','this.parentNode.offsetHeight + "px"');if(full)
s.setExpression('width','jQuery.support.boxModel && document.documentElement.clientWidth || document.body.clientWidth + "px"');else
s.setExpression('width','this.parentNode.offsetWidth + "px"');if(fixL)s.setExpression('left',fixL);if(fixT)s.setExpression('top',fixT);}
else if(opts.centerY){if(full)s.setExpression('top','(document.documentElement.clientHeight || document.body.clientHeight) / 2 - (this.offsetHeight / 2) + (blah = document.documentElement.scrollTop ? document.documentElement.scrollTop : document.body.scrollTop) + "px"');s.marginTop=0;}
else if(!opts.centerY&&full){var top=(opts.css&&opts.css.top)?parseInt(opts.css.top,10):0;var expression='((document.documentElement.scrollTop ? document.documentElement.scrollTop : document.body.scrollTop) + '+top+') + "px"';s.setExpression('top',expression);}});}
if(msg){if(opts.theme)
lyr3.find('.ui-widget-content').append(msg);else
lyr3.append(msg);if(msg.jquery||msg.nodeType)
$(msg).show();}
if((msie||opts.forceIframe)&&opts.showOverlay)
lyr1.show();if(opts.fadeIn){var cb=opts.onBlock?opts.onBlock:noOp;var cb1=(opts.showOverlay&&!msg)?cb:noOp;var cb2=msg?cb:noOp;if(opts.showOverlay)
lyr2._fadeIn(opts.fadeIn,cb1);if(msg)
lyr3._fadeIn(opts.fadeIn,cb2);}
else{if(opts.showOverlay)
lyr2.show();if(msg)
lyr3.show();if(opts.onBlock)
opts.onBlock.bind(lyr3)();}
bind(1,el,opts);if(full){pageBlock=lyr3[0];pageBlockEls=$(opts.focusableElements,pageBlock);if(opts.focusInput)
setTimeout(focus,20);}
else
center(lyr3[0],opts.centerX,opts.centerY);if(opts.timeout){var to=setTimeout(function(){if(full)
$.unblockUI(opts);else
$(el).unblock(opts);},opts.timeout);$(el).data('blockUI.timeout',to);}}
function remove(el,opts){var count;var full=(el==window);var $el=$(el);var data=$el.data('blockUI.history');var to=$el.data('blockUI.timeout');if(to){clearTimeout(to);$el.removeData('blockUI.timeout');}
opts=$.extend({},$.blockUI.defaults,opts||{});bind(0,el,opts);if(opts.onUnblock===null){opts.onUnblock=$el.data('blockUI.onUnblock');$el.removeData('blockUI.onUnblock');}
var els;if(full)
els=$('body').children().filter('.blockUI').add('body > .blockUI');else
els=$el.find('>.blockUI');if(opts.cursorReset){if(els.length>1)
els[1].style.cursor=opts.cursorReset;if(els.length>2)
els[2].style.cursor=opts.cursorReset;}
if(full)
pageBlock=pageBlockEls=null;if(opts.fadeOut){count=els.length;els.stop().fadeOut(opts.fadeOut,function(){if(--count===0)
reset(els,data,opts,el);});}
else
reset(els,data,opts,el);}
function reset(els,data,opts,el){var $el=$(el);if($el.data('blockUI.isBlocked'))
return;els.each(function(i,o){if(this.parentNode)
this.parentNode.removeChild(this);});if(data&&data.el){data.el.style.display=data.display;data.el.style.position=data.position;data.el.style.cursor='default';if(data.parent)
data.parent.appendChild(data.el);$el.removeData('blockUI.history');}
if($el.data('blockUI.static')){$el.css('position','static');}
if(typeof opts.onUnblock=='function')
opts.onUnblock(el,opts);var body=$(document.body),w=body.width(),cssW=body[0].style.width;body.width(w-1).width(w);body[0].style.width=cssW;}
function bind(b,el,opts){var full=el==window,$el=$(el);if(!b&&(full&&!pageBlock||!full&&!$el.data('blockUI.isBlocked')))
return;$el.data('blockUI.isBlocked',b);if(!full||!opts.bindEvents||(b&&!opts.showOverlay))
return;var events='mousedown mouseup keydown keypress keyup touchstart touchend touchmove';if(b)
$(document).bind(events,opts,handler);else
$(document).unbind(events,handler);}
function handler(e){if(e.type==='keydown'&&e.keyCode&&e.keyCode==9){if(pageBlock&&e.data.constrainTabKey){var els=pageBlockEls;var fwd=!e.shiftKey&&e.target===els[els.length-1];var back=e.shiftKey&&e.target===els[0];if(fwd||back){setTimeout(function(){focus(back);},10);return false;}}}
var opts=e.data;var target=$(e.target);if(target.hasClass('blockOverlay')&&opts.onOverlayClick)
opts.onOverlayClick(e);if(target.parents('div.'+opts.blockMsgClass).length>0)
return true;return target.parents().children().filter('div.blockUI').length===0;}
function focus(back){if(!pageBlockEls)
return;var e=pageBlockEls[back===true?pageBlockEls.length-1:0];if(e)
e.focus();}
function center(el,x,y){var p=el.parentNode,s=el.style;var l=((p.offsetWidth-el.offsetWidth)/2)-sz(p,'borderLeftWidth');var t=((p.offsetHeight-el.offsetHeight)/2)-sz(p,'borderTopWidth');if(x)s.left=l>0?(l+'px'):'0';if(y)s.top=t>0?(t+'px'):'0';}
function sz(el,p){return parseInt($.css(el,p),10)||0;}}
if(typeof define==='function'&&define.amd&&define.amd.jQuery){define(['jquery'],setup);}else{setup(jQuery);}})();(function(factory){"use strict";if(typeof define==='function'&&define.amd){define(['jquery'],factory);}else{factory((typeof(jQuery)!='undefined')?jQuery:window.Zepto);}}
(function($){"use strict";var feature={};feature.fileapi=$("<input type='file'/>").get(0).files!==undefined;feature.formdata=window.FormData!==undefined;var hasProp=!!$.fn.prop;$.fn.attr2=function(){if(!hasProp){return this.attr.apply(this,arguments);}
var val=this.prop.apply(this,arguments);if((val&&val.jquery)||typeof val==='string'){return val;}
return this.attr.apply(this,arguments);};$.fn.ajaxSubmit=function(options){if(!this.length){log('ajaxSubmit: skipping submit process - no element selected');return this;}
var method,action,url,$form=this;if(typeof options=='function'){options={success:options};}
else if(options===undefined){options={};}
method=options.type||this.attr2('method');action=options.url||this.attr2('action');url=(typeof action==='string')?$.trim(action):'';url=url||window.location.href||'';if(url){url=(url.match(/^([^#]+)/)||[])[1];}
options=$.extend(true,{url:url,success:$.ajaxSettings.success,type:method||$.ajaxSettings.type,iframeSrc:/^https/i.test(window.location.href||'')?'javascript:false':'about:blank'},options);var veto={};this.trigger('form-pre-serialize',[this,options,veto]);if(veto.veto){log('ajaxSubmit: submit vetoed via form-pre-serialize trigger');return this;}
if(options.beforeSerialize&&options.beforeSerialize(this,options)===false){log('ajaxSubmit: submit aborted via beforeSerialize callback');return this;}
var traditional=options.traditional;if(traditional===undefined){traditional=$.ajaxSettings.traditional;}
var elements=[];var qx,a=this.formToArray(options.semantic,elements);if(options.data){options.extraData=options.data;qx=$.param(options.data,traditional);}
if(options.beforeSubmit&&options.beforeSubmit(a,this,options)===false){log('ajaxSubmit: submit aborted via beforeSubmit callback');return this;}
this.trigger('form-submit-validate',[a,this,options,veto]);if(veto.veto){log('ajaxSubmit: submit vetoed via form-submit-validate trigger');return this;}
var q=$.param(a,traditional);if(qx){q=(q?(q+'&'+qx):qx);}
if(options.type.toUpperCase()=='GET'){options.url+=(options.url.indexOf('?')>=0?'&':'?')+q;options.data=null;}
else{options.data=q;}
var callbacks=[];if(options.resetForm){callbacks.push(function(){$form.resetForm();});}
if(options.clearForm){callbacks.push(function(){$form.clearForm(options.includeHidden);});}
if(!options.dataType&&options.target){var oldSuccess=options.success||function(){};callbacks.push(function(data){var fn=options.replaceTarget?'replaceWith':'html';$(options.target)[fn](data).each(oldSuccess,arguments);});}
else if(options.success){callbacks.push(options.success);}
options.success=function(data,status,xhr){var context=options.context||this;for(var i=0,max=callbacks.length;i<max;i++){callbacks[i].apply(context,[data,status,xhr||$form,$form]);}};if(options.error){var oldError=options.error;options.error=function(xhr,status,error){var context=options.context||this;oldError.apply(context,[xhr,status,error,$form]);};}
if(options.complete){var oldComplete=options.complete;options.complete=function(xhr,status){var context=options.context||this;oldComplete.apply(context,[xhr,status,$form]);};}
var fileInputs=$('input[type=file]:enabled',this).filter(function(){return $(this).val()!=='';});var hasFileInputs=fileInputs.length>0;var mp='multipart/form-data';var multipart=($form.attr('enctype')==mp||$form.attr('encoding')==mp);var fileAPI=feature.fileapi&&feature.formdata;log("fileAPI :"+fileAPI);var shouldUseFrame=(hasFileInputs||multipart)&&!fileAPI;var jqxhr;if(options.iframe!==false&&(options.iframe||shouldUseFrame)){if(options.closeKeepAlive){$.get(options.closeKeepAlive,function(){jqxhr=fileUploadIframe(a);});}
else{jqxhr=fileUploadIframe(a);}}
else if((hasFileInputs||multipart)&&fileAPI){jqxhr=fileUploadXhr(a);}
else{jqxhr=$.ajax(options);}
$form.removeData('jqxhr').data('jqxhr',jqxhr);for(var k=0;k<elements.length;k++){elements[k]=null;}
this.trigger('form-submit-notify',[this,options]);return this;function deepSerialize(extraData){var serialized=$.param(extraData,options.traditional).split('&');var len=serialized.length;var result=[];var i,part;for(i=0;i<len;i++){serialized[i]=serialized[i].replace(/\+/g,' ');part=serialized[i].split('=');result.push([decodeURIComponent(part[0]),decodeURIComponent(part[1])]);}
return result;}
function fileUploadXhr(a){var formdata=new FormData();for(var i=0;i<a.length;i++){formdata.append(a[i].name,a[i].value);}
if(options.extraData){var serializedData=deepSerialize(options.extraData);for(i=0;i<serializedData.length;i++){if(serializedData[i]){formdata.append(serializedData[i][0],serializedData[i][1]);}}}
options.data=null;var s=$.extend(true,{},$.ajaxSettings,options,{contentType:false,processData:false,cache:false,type:method||'POST'});if(options.uploadProgress){s.xhr=function(){var xhr=$.ajaxSettings.xhr();if(xhr.upload){xhr.upload.addEventListener('progress',function(event){var percent=0;var position=event.loaded||event.position;var total=event.total;if(event.lengthComputable){percent=Math.ceil(position/total*100);}
options.uploadProgress(event,position,total,percent);},false);}
return xhr;};}
s.data=null;var beforeSend=s.beforeSend;s.beforeSend=function(xhr,o){if(options.formData){o.data=options.formData;}
else{o.data=formdata;}
if(beforeSend){beforeSend.call(this,xhr,o);}};return $.ajax(s);}
function fileUploadIframe(a){var form=$form[0],el,i,s,g,id,$io,io,xhr,sub,n,timedOut,timeoutHandle;var deferred=$.Deferred();deferred.abort=function(status){xhr.abort(status);};if(a){for(i=0;i<elements.length;i++){el=$(elements[i]);if(hasProp){el.prop('disabled',false);}
else{el.removeAttr('disabled');}}}
s=$.extend(true,{},$.ajaxSettings,options);s.context=s.context||s;id='jqFormIO'+(new Date().getTime());if(s.iframeTarget){$io=$(s.iframeTarget);n=$io.attr2('name');if(!n){$io.attr2('name',id);}
else{id=n;}}
else{$io=$('<iframe name="'+id+'" src="'+s.iframeSrc+'" />');$io.css({position:'absolute',top:'-1000px',left:'-1000px'});}
io=$io[0];xhr={aborted:0,responseText:null,responseXML:null,status:0,statusText:'n/a',getAllResponseHeaders:function(){},getResponseHeader:function(){},setRequestHeader:function(){},abort:function(status){var e=(status==='timeout'?'timeout':'aborted');log('aborting upload... '+e);this.aborted=1;try{if(io.contentWindow.document.execCommand){io.contentWindow.document.execCommand('Stop');}}
catch(ignore){}
$io.attr('src',s.iframeSrc);xhr.error=e;if(s.error){s.error.call(s.context,xhr,e,status);}
if(g){$.event.trigger("ajaxError",[xhr,s,e]);}
if(s.complete){s.complete.call(s.context,xhr,e);}}};g=s.global;if(g&&0===$.active++){$.event.trigger("ajaxStart");}
if(g){$.event.trigger("ajaxSend",[xhr,s]);}
if(s.beforeSend&&s.beforeSend.call(s.context,xhr,s)===false){if(s.global){$.active--;}
deferred.reject();return deferred;}
if(xhr.aborted){deferred.reject();return deferred;}
sub=form.clk;if(sub){n=sub.name;if(n&&!sub.disabled){s.extraData=s.extraData||{};s.extraData[n]=sub.value;if(sub.type=="image"){s.extraData[n+'.x']=form.clk_x;s.extraData[n+'.y']=form.clk_y;}}}
var CLIENT_TIMEOUT_ABORT=1;var SERVER_ABORT=2;function getDoc(frame){var doc=null;try{if(frame.contentWindow){doc=frame.contentWindow.document;}}catch(err){log('cannot get iframe.contentWindow document: '+err);}
if(doc){return doc;}
try{doc=frame.contentDocument?frame.contentDocument:frame.document;}catch(err){log('cannot get iframe.contentDocument: '+err);doc=frame.document;}
return doc;}
var csrf_token=$('meta[name=csrf-token]').attr('content');var csrf_param=$('meta[name=csrf-param]').attr('content');if(csrf_param&&csrf_token){s.extraData=s.extraData||{};s.extraData[csrf_param]=csrf_token;}
function doSubmit(){var t=$form.attr2('target'),a=$form.attr2('action'),mp='multipart/form-data',et=$form.attr('enctype')||$form.attr('encoding')||mp;form.setAttribute('target',id);if(!method||/post/i.test(method)){form.setAttribute('method','POST');}
if(a!=s.url){form.setAttribute('action',s.url);}
if(!s.skipEncodingOverride&&(!method||/post/i.test(method))){$form.attr({encoding:'multipart/form-data',enctype:'multipart/form-data'});}
if(s.timeout){timeoutHandle=setTimeout(function(){timedOut=true;cb(CLIENT_TIMEOUT_ABORT);},s.timeout);}
function checkState(){try{var state=getDoc(io).readyState;log('state = '+state);if(state&&state.toLowerCase()=='uninitialized'){setTimeout(checkState,50);}}
catch(e){log('Server abort: ',e,' (',e.name,')');cb(SERVER_ABORT);if(timeoutHandle){clearTimeout(timeoutHandle);}
timeoutHandle=undefined;}}
var extraInputs=[];try{if(s.extraData){for(var n in s.extraData){if(s.extraData.hasOwnProperty(n)){if($.isPlainObject(s.extraData[n])&&s.extraData[n].hasOwnProperty('name')&&s.extraData[n].hasOwnProperty('value')){extraInputs.push($('<input type="hidden" name="'+s.extraData[n].name+'">').val(s.extraData[n].value).appendTo(form)[0]);}else{extraInputs.push($('<input type="hidden" name="'+n+'">').val(s.extraData[n]).appendTo(form)[0]);}}}}
if(!s.iframeTarget){$io.appendTo('body');}
if(io.attachEvent){io.attachEvent('onload',cb);}
else{io.addEventListener('load',cb,false);}
setTimeout(checkState,15);try{form.submit();}catch(err){var submitFn=document.createElement('form').submit;submitFn.apply(form);}}
finally{form.setAttribute('action',a);form.setAttribute('enctype',et);if(t){form.setAttribute('target',t);}else{$form.removeAttr('target');}
$(extraInputs).remove();}}
if(s.forceSync){doSubmit();}
else{setTimeout(doSubmit,10);}
var data,doc,domCheckCount=50,callbackProcessed;function cb(e){if(xhr.aborted||callbackProcessed){return;}
doc=getDoc(io);if(!doc){log('cannot access response document');e=SERVER_ABORT;}
if(e===CLIENT_TIMEOUT_ABORT&&xhr){xhr.abort('timeout');deferred.reject(xhr,'timeout');return;}
else if(e==SERVER_ABORT&&xhr){xhr.abort('server abort');deferred.reject(xhr,'error','server abort');return;}
if(!doc||doc.location.href==s.iframeSrc){if(!timedOut){return;}}
if(io.detachEvent){io.detachEvent('onload',cb);}
else{io.removeEventListener('load',cb,false);}
var status='success',errMsg;try{if(timedOut){throw'timeout';}
var isXml=s.dataType=='xml'||doc.XMLDocument||$.isXMLDoc(doc);log('isXml='+isXml);if(!isXml&&window.opera&&(doc.body===null||!doc.body.innerHTML)){if(--domCheckCount){log('requeing onLoad callback, DOM not available');setTimeout(cb,250);return;}}
var docRoot=doc.body?doc.body:doc.documentElement;xhr.responseText=docRoot?docRoot.innerHTML:null;xhr.responseXML=doc.XMLDocument?doc.XMLDocument:doc;if(isXml){s.dataType='xml';}
xhr.getResponseHeader=function(header){var headers={'content-type':s.dataType};return headers[header.toLowerCase()];};if(docRoot){xhr.status=Number(docRoot.getAttribute('status'))||xhr.status;xhr.statusText=docRoot.getAttribute('statusText')||xhr.statusText;}
var dt=(s.dataType||'').toLowerCase();var scr=/(json|script|text)/.test(dt);if(scr||s.textarea){var ta=doc.getElementsByTagName('textarea')[0];if(ta){xhr.responseText=ta.value;xhr.status=Number(ta.getAttribute('status'))||xhr.status;xhr.statusText=ta.getAttribute('statusText')||xhr.statusText;}
else if(scr){var pre=doc.getElementsByTagName('pre')[0];var b=doc.getElementsByTagName('body')[0];if(pre){xhr.responseText=pre.textContent?pre.textContent:pre.innerText;}
else if(b){xhr.responseText=b.textContent?b.textContent:b.innerText;}}}
else if(dt=='xml'&&!xhr.responseXML&&xhr.responseText){xhr.responseXML=toXml(xhr.responseText);}
try{data=httpData(xhr,dt,s);}
catch(err){status='parsererror';xhr.error=errMsg=(err||status);}}
catch(err){log('error caught: ',err);status='error';xhr.error=errMsg=(err||status);}
if(xhr.aborted){log('upload aborted');status=null;}
if(xhr.status){status=(xhr.status>=200&&xhr.status<300||xhr.status===304)?'success':'error';}
if(status==='success'){if(s.success){s.success.call(s.context,data,'success',xhr);}
deferred.resolve(xhr.responseText,'success',xhr);if(g){$.event.trigger("ajaxSuccess",[xhr,s]);}}
else if(status){if(errMsg===undefined){errMsg=xhr.statusText;}
if(s.error){s.error.call(s.context,xhr,status,errMsg);}
deferred.reject(xhr,'error',errMsg);if(g){$.event.trigger("ajaxError",[xhr,s,errMsg]);}}
if(g){$.event.trigger("ajaxComplete",[xhr,s]);}
if(g&&!--$.active){$.event.trigger("ajaxStop");}
if(s.complete){s.complete.call(s.context,xhr,status);}
callbackProcessed=true;if(s.timeout){clearTimeout(timeoutHandle);}
setTimeout(function(){if(!s.iframeTarget){$io.remove();}
else{$io.attr('src',s.iframeSrc);}
xhr.responseXML=null;},100);}
var toXml=$.parseXML||function(s,doc){if(window.ActiveXObject){doc=new ActiveXObject('Microsoft.XMLDOM');doc.async='false';doc.loadXML(s);}
else{doc=(new DOMParser()).parseFromString(s,'text/xml');}
return(doc&&doc.documentElement&&doc.documentElement.nodeName!='parsererror')?doc:null;};var parseJSON=$.parseJSON||function(s){return window['eval']('('+s+')');};var httpData=function(xhr,type,s){var ct=xhr.getResponseHeader('content-type')||'',xml=type==='xml'||!type&&ct.indexOf('xml')>=0,data=xml?xhr.responseXML:xhr.responseText;if(xml&&data.documentElement.nodeName==='parsererror'){if($.error){$.error('parsererror');}}
if(s&&s.dataFilter){data=s.dataFilter(data,type);}
if(typeof data==='string'){if(type==='json'||!type&&ct.indexOf('json')>=0){data=parseJSON(data);}else if(type==="script"||!type&&ct.indexOf("javascript")>=0){$.globalEval(data);}}
return data;};return deferred;}};$.fn.ajaxForm=function(options){options=options||{};options.delegation=options.delegation&&$.isFunction($.fn.on);if(!options.delegation&&this.length===0){var o={s:this.selector,c:this.context};if(!$.isReady&&o.s){log('DOM not ready, queuing ajaxForm');$(function(){$(o.s,o.c).ajaxForm(options);});return this;}
log('terminating; zero elements found by selector'+($.isReady?'':' (DOM not ready)'));return this;}
if(options.delegation){$(document).off('submit.form-plugin',this.selector,doAjaxSubmit).off('click.form-plugin',this.selector,captureSubmittingElement).on('submit.form-plugin',this.selector,options,doAjaxSubmit).on('click.form-plugin',this.selector,options,captureSubmittingElement);return this;}
return this.ajaxFormUnbind().bind('submit.form-plugin',options,doAjaxSubmit).bind('click.form-plugin',options,captureSubmittingElement);};function doAjaxSubmit(e){var options=e.data;if(!e.isDefaultPrevented()){e.preventDefault();$(e.target).ajaxSubmit(options);}}
function captureSubmittingElement(e){var target=e.target;var $el=$(target);if(!($el.is("[type=submit],[type=image]"))){var t=$el.closest('[type=submit]');if(t.length===0){return;}
target=t[0];}
var form=this;form.clk=target;if(target.type=='image'){if(e.offsetX!==undefined){form.clk_x=e.offsetX;form.clk_y=e.offsetY;}else if(typeof $.fn.offset=='function'){var offset=$el.offset();form.clk_x=e.pageX-offset.left;form.clk_y=e.pageY-offset.top;}else{form.clk_x=e.pageX-target.offsetLeft;form.clk_y=e.pageY-target.offsetTop;}}
setTimeout(function(){form.clk=form.clk_x=form.clk_y=null;},100);}
$.fn.ajaxFormUnbind=function(){return this.unbind('submit.form-plugin click.form-plugin');};$.fn.formToArray=function(semantic,elements){var a=[];if(this.length===0){return a;}
var form=this[0];var formId=this.attr('id');var els=semantic?form.getElementsByTagName('*'):form.elements;var els2;if(els&&!/MSIE [678]/.test(navigator.userAgent)){els=$(els).get();}
if(formId){els2=$(':input[form="'+formId+'"]').get();if(els2.length){els=(els||[]).concat(els2);}}
if(!els||!els.length){return a;}
var i,j,n,v,el,max,jmax;for(i=0,max=els.length;i<max;i++){el=els[i];n=el.name;if(!n||el.disabled){continue;}
if(semantic&&form.clk&&el.type=="image"){if(form.clk==el){a.push({name:n,value:$(el).val(),type:el.type});a.push({name:n+'.x',value:form.clk_x},{name:n+'.y',value:form.clk_y});}
continue;}
v=$.fieldValue(el,true);if(v&&v.constructor==Array){if(elements){elements.push(el);}
for(j=0,jmax=v.length;j<jmax;j++){a.push({name:n,value:v[j]});}}
else if(feature.fileapi&&el.type=='file'){if(elements){elements.push(el);}
var files=el.files;if(files.length){for(j=0;j<files.length;j++){a.push({name:n,value:files[j],type:el.type});}}
else{a.push({name:n,value:'',type:el.type});}}
else if(v!==null&&typeof v!='undefined'){if(elements){elements.push(el);}
a.push({name:n,value:v,type:el.type,required:el.required});}}
if(!semantic&&form.clk){var $input=$(form.clk),input=$input[0];n=input.name;if(n&&!input.disabled&&input.type=='image'){a.push({name:n,value:$input.val()});a.push({name:n+'.x',value:form.clk_x},{name:n+'.y',value:form.clk_y});}}
return a;};$.fn.formSerialize=function(semantic){return $.param(this.formToArray(semantic));};$.fn.fieldSerialize=function(successful){var a=[];this.each(function(){var n=this.name;if(!n){return;}
var v=$.fieldValue(this,successful);if(v&&v.constructor==Array){for(var i=0,max=v.length;i<max;i++){a.push({name:n,value:v[i]});}}
else if(v!==null&&typeof v!='undefined'){a.push({name:this.name,value:v});}});return $.param(a);};$.fn.fieldValue=function(successful){for(var val=[],i=0,max=this.length;i<max;i++){var el=this[i];var v=$.fieldValue(el,successful);if(v===null||typeof v=='undefined'||(v.constructor==Array&&!v.length)){continue;}
if(v.constructor==Array){$.merge(val,v);}
else{val.push(v);}}
return val;};$.fieldValue=function(el,successful){var n=el.name,t=el.type,tag=el.tagName.toLowerCase();if(successful===undefined){successful=true;}
if(successful&&(!n||el.disabled||t=='reset'||t=='button'||(t=='checkbox'||t=='radio')&&!el.checked||(t=='submit'||t=='image')&&el.form&&el.form.clk!=el||tag=='select'&&el.selectedIndex==-1)){return null;}
if(tag=='select'){var index=el.selectedIndex;if(index<0){return null;}
var a=[],ops=el.options;var one=(t=='select-one');var max=(one?index+1:ops.length);for(var i=(one?index:0);i<max;i++){var op=ops[i];if(op.selected){var v=op.value;if(!v){v=(op.attributes&&op.attributes.value&&!(op.attributes.value.specified))?op.text:op.value;}
if(one){return v;}
a.push(v);}}
return a;}
return $(el).val();};$.fn.clearForm=function(includeHidden){return this.each(function(){$('input,select,textarea',this).clearFields(includeHidden);});};$.fn.clearFields=$.fn.clearInputs=function(includeHidden){var re=/^(?:color|date|datetime|email|month|number|password|range|search|tel|text|time|url|week)$/i;return this.each(function(){var t=this.type,tag=this.tagName.toLowerCase();if(re.test(t)||tag=='textarea'){this.value='';}
else if(t=='checkbox'||t=='radio'){this.checked=false;}
else if(tag=='select'){this.selectedIndex=-1;}
else if(t=="file"){if(/MSIE/.test(navigator.userAgent)){$(this).replaceWith($(this).clone(true));}else{$(this).val('');}}
else if(includeHidden){if((includeHidden===true&&/hidden/.test(t))||(typeof includeHidden=='string'&&$(this).is(includeHidden))){this.value='';}}});};$.fn.resetForm=function(){return this.each(function(){if(typeof this.reset=='function'||(typeof this.reset=='object'&&!this.reset.nodeType)){this.reset();}});};$.fn.enable=function(b){if(b===undefined){b=true;}
return this.each(function(){this.disabled=!b;});};$.fn.selected=function(select){if(select===undefined){select=true;}
return this.each(function(){var t=this.type;if(t=='checkbox'||t=='radio'){this.checked=select;}
else if(this.tagName.toLowerCase()=='option'){var $sel=$(this).parent('select');if(select&&$sel[0]&&$sel[0].type=='select-one'){$sel.find('option').selected(false);}
this.selected=select;}});};$.fn.ajaxSubmit.debug=false;function log(){if(!$.fn.ajaxSubmit.debug){return;}
var msg='[jquery.form] '+Array.prototype.join.call(arguments,'');if(window.console&&window.console.log){window.console.log(msg);}
else if(window.opera&&window.opera.postError){window.opera.postError(msg);}}}));(function($){$.caretTo=function(el,index){if(el.createTextRange){var range=el.createTextRange();range.move("character",index);range.select();}else if(el.selectionStart!=null){el.focus();el.setSelectionRange(index,index);}};$.caretPos=function(el){if("selection"in document){var range=el.createTextRange();try{range.setEndPoint("EndToStart",document.selection.createRange());}catch(e){return 0;}
return range.text.length;}else if(el.selectionStart!=null){return el.selectionStart;}};$.fn.caret=function(index,offset){if(typeof(index)==="undefined"){return $.caretPos(this.get(0));}
return this.queue(function(next){if(isNaN(index)){var i=$(this).val().indexOf(index);if(offset===true){i+=index.length;}else if(typeof(offset)!=="undefined"){i+=offset;}
$.caretTo(this,i);}else{$.caretTo(this,index);}
next();});};$.fn.caretToStart=function(){return this.caret(0);};$.fn.caretToEnd=function(){return this.queue(function(next){$.caretTo(this,$(this).val().length);next();});};}(jQuery));(function(factory){if(typeof define==='function'&&define.amd){define(['jquery'],factory);}else if(typeof exports==='object'){module.exports=factory(require('jquery'));}else{factory(jQuery);}}(function($){var pluses=/\+/g;function encode(s){return config.raw?s:encodeURIComponent(s);}
function decode(s){return config.raw?s:decodeURIComponent(s);}
function stringifyCookieValue(value){return encode(config.json?JSON.stringify(value):String(value));}
function parseCookieValue(s){if(s.indexOf('"')===0){s=s.slice(1,-1).replace(/\\"/g,'"').replace(/\\\\/g,'\\');}
try{s=decodeURIComponent(s.replace(pluses,' '));return config.json?JSON.parse(s):s;}catch(e){}}
function read(s,converter){var value=config.raw?s:parseCookieValue(s);return $.isFunction(converter)?converter(value):value;}
var config=$.cookie=function(key,value,options){if(arguments.length>1&&!$.isFunction(value)){options=$.extend({},config.defaults,options);if(typeof options.expires==='number'){var days=options.expires,t=options.expires=new Date();t.setMilliseconds(t.getMilliseconds()+days*864e+5);}
return(document.cookie=[encode(key),'=',stringifyCookieValue(value),options.expires?'; expires='+options.expires.toUTCString():'',options.path?'; path='+options.path:'',options.domain?'; domain='+options.domain:'',options.secure?'; secure':''].join(''));}
var result=key?undefined:{},cookies=document.cookie?document.cookie.split('; '):[],i=0,l=cookies.length;for(;i<l;i++){var parts=cookies[i].split('='),name=decode(parts.shift()),cookie=parts.join('=');if(key===name){result=read(cookie,value);break;}
if(!key&&(cookie=read(cookie))!==undefined){result[name]=cookie;}}
return result;};config.defaults={};$.removeCookie=function(key,options){$.cookie(key,'',$.extend({},options,{expires:-1}));return!$.cookie(key);};}));(function(global){"use strict";var __JU,i,j,gVar,parts,curPart,curObj,_autoPopulateGlobal=true,VERSION='v1.01.0',TYPE='JsUtils';if(global.gettext===undefined){global.gettext=function(s){if(s==undefined){return'';}
return s;};}
function _removeFromVersionQueue(versionString){var index=global.JU._versionQueue.indexOf(versionString);if(index>-1){global.JU._versionQueue.splice(index,1);}}
if(!global.JU&&global.hasOwnProperty('JU_autoPopulateGlobal'))
{_autoPopulateGlobal=!!global['JU_autoPopulateGlobal'];}
global.JU=global.JU||{'_repo':[],'_versionQueue':[],'_autoPopulateGlobal':_autoPopulateGlobal,'_version':VERSION,activate:function(target,versionString)
{var i,gVar,ju=global.JU.get(versionString),property;if(!ju||!target){return false;}
_removeFromVersionQueue(versionString);global.JU._versionQueue.push(ju.version);for(property in ju){if(ju.hasOwnProperty(property)){target[property]=ju[property];}}
return true;},deactivate:function(target,versionString){if(!target){return false;}
var removeAll=false,ju,i,gVar;if(versionString=='*'){removeAll=true;versionString=null;}
ju=global.JU.get(versionString);if(!ju){return false;}
for(i=0;i<ju._globalVars.length;i++){gVar=ju._globalVars[i];if(gVar&&gVar.indexOf('.')==-1&&target.hasOwnProperty(gVar)&&(target[gVar].hasOwnProperty('type')&&target[gVar].type==TYPE)&&(removeAll||target[gVar].version==versionString))
{delete target[gVar];}}
return true;},publish:function(ju,populateGlobals,forcePush){var version=ju.version,_repo=global.JU._repo;if(global.JU.get(version)&&forcePush){global.JU.remove(version);}
if(!global.JU.get(version)){_repo.push(ju);_repo.sort(function(a,b){if(''.localeCompare){return a.toString().localeCompare(b.toString());}
if(a.toString()<b.toString()){return-1;}
if(a.toString()>b.toString()){return 1;}
return 0;});}
if(populateGlobals){global.JU.activate(global,version);}},get:function(versionString)
{var i,_repo=global.JU._repo;if(!_repo){return null;}
if(!versionString){return _repo[_repo.length-1];}
for(i=0;i<_repo.length;i++){if(_repo[i].version==versionString){return _repo[i];}}
return null;},remove:function(versionString){var i,_repo=global.JU._repo,ju;if(!_repo){return null;}
if(!versionString){ju=global.JU.get();if(!ju){return null;}
versionString=ju.version;}
for(i=0;i<_repo.length;i++){if(_repo[i].version==versionString){_removeFromVersionQueue(versionString);global.JU.deactivate(global,versionString);return _repo.splice(i,1);}}
return null;},revert:function(populateGlobals){var _repo=global.JU._repo,queue=global.JU._versionQueue,version,ju;if(_repo.length>0&&queue.length>0){version=queue.pop();while(queue.length){ju=global.JU.get(version);if(!ju){version=queue.pop();continue;}
global.JU.deactivate(global,version);if(populateGlobals&&queue.length){version=queue[queue.length-1];global.JU.activate(global,version);}
return ju;}}
return null;}};__JU={'_globalVars':['Arr','Dt','Fn','Obj','Pref','Slct','Stl','Str','Tmr','Typ','UI','UI.Bs','UI.Patterns','Utl'],'version':VERSION,'type':TYPE};for(i=0;i<__JU._globalVars.length;i++){gVar=__JU._globalVars[i];if(gVar){if(gVar.indexOf('.')==-1){__JU[gVar]={'version':VERSION,'class':gVar,'type':TYPE}}
else{curObj=__JU;parts=gVar.split('.');for(j=0;j<parts.length;j++){curPart=parts[j];if(!curObj.hasOwnProperty(curPart)){curObj[curPart]={'version':VERSION,'class':curPart,'type':TYPE};}
curObj=curObj[curPart];}}}}
global.JU.__JU=__JU;}(typeof window!=='undefined'?window:this));(function(global,Tmr){"use strict";Tmr.run=function(func,delay,thisArg){return setTimeout(function(){func.call(thisArg||this);},delay);};}(typeof window!=='undefined'?window:this,JU.__JU.Tmr));(function(global,$,Dt){"use strict";var _dayShort=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],_dayLong=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'],_dayViet=['Thứ Hai','Thứ Ba','Thứ Tư','Thứ Năm','Thứ Sáu','Thứ Bảy','Chúa Nhật'],_monthShort=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],_monthLong=['January','February','March','April','May','June','July','August','September','October','November','December'];Dt.getDateParts=function(d){var o={},j=d.getDate(),w=d.getDay(),GG=d.getHours(),n=d.getMonth(),Y=d.getFullYear(),g=GG<=12?GG:GG-12,tz=d.getTimezoneOffset()/60,tzSign=tz<0?'-':'+';g=g==0?12:g;tz=Math.abs(tz);o.d=Dt.padZero(j);o.D=_dayShort[w];o.j=j;o.l=_dayLong[w];o.N=_dayViet[w];o.F=_monthLong[n];o.m=Dt.padZero(n+1);o.M=_monthShort[n];o.n=n+1;o.T='Tháng '+(n+1);o.Y=Y;o.y=Y.toString().substring(2);o.a=GG<12?'am':'pm';o.A=GG<12?'AM':'PM';o.g=g;o.G=GG;o.h=Dt.padZero(g);o.H=Dt.padZero(GG);o.i=Dt.padZero(d.getMinutes());o.s=Dt.padZero(d.getSeconds());o.O=tzSign+Dt.padZero(tz)+'00';o.P=tzSign+Dt.padZero(tz)+':00';o.c=o.Y+'-'+o.m+'-'+o.d+' '+o.H+':'+o.i+':'+o.s+o.P;o.r=o.D+', '+o.j+' '+o.M+' '+o.Y+' '+o.H+':'+o.i+':'+o.s+' '+o.O;o.q=o.Y+'-'+o.m+'-'+o.d+' '+o.H+':'+o.i+':'+o.s;o.o=o.Y+'-'+o.m+'-'+o.d;o.t=o.g+':'+o.i+o.a;return o;};Dt.getUtcParts=function(d){var utc=Dt.toUtc(d),o=Dt.getDateParts(utc);o.O='+0000';o.P='+00:00';o.c=o.c.substring(0,19)+o.O;o.r=o.r.substring(0,26)+o.P;return o;};Dt.toUtc=function(d)
{var offset=d.getTimezoneOffset()*60000;return new Date(d.getTime()+offset);};Dt.isSameDate=function(d1,d2)
{return d1.getFullYear()==d2.getFullYear()&&d1.getMonth()==d2.getMonth()&&d1.getDate()==d2.getDate();};Dt.epochSameDate=function(e1,e2){var d1=new Date(e1),d2=new Date(e2);return Dt.isSameDate(d1,d2);};Dt.padZero=function(s){s=s.toString();return s.length==2?s:'0'+s;};Dt.isDate=function(o){return Object.prototype.toString.call(o)==="[object Date]";};Dt.isValid=function(d){if(Dt.isDate(d)){return!isNaN(d.getTime());}
return false;};Dt.format=function(d,format){if(!Dt.isValid(d)){return format;}
var p=Dt.getDateParts(d),result=format.replace(/(\\?)([dDjlNFmMnTYyaAgGhHisOPcrqot])/g,function(whole,slash,key){if(!slash){return p[key];}
return key;});result=result.replace(/\\([a-z])/gi,'$1');return result;};}(typeof window!=='undefined'?window:this,jQuery,JU.__JU.Dt));(function(global,$,Obj){"use strict";Obj.pop=function(obj,prop,defaultValue){if(!obj.hasOwnProperty(prop)){return defaultValue}
var result=obj[prop];delete obj[prop];return result;};Obj.hasProp=function(obj,prop){return obj.hasOwnProperty(prop);}}(typeof window!=='undefined'?window:this,jQuery,JU.__JU.Obj));(function(global,$,Typ){"use strict";Typ.isJquery=function(o){return o instanceof jQuery;};Typ.isObj=function(o){return $.type(o)==='object';};Typ.isStr=function(o){return $.type(o)==='string';};Typ.isFunc=function(o){return $.type(o)==='function';};Typ.isRegex=function(o){return $.type(o)==='regexp';};Typ.isNumber=function(o){return $.type(o)==='number';};Typ.isInt=function(o){return Typ.isNumber(o)&&o%1===0;};Typ.isFloat=function(o){return Typ.isNumber(o)&&!Typ.isInt(o);};Typ.isDate=function(o){return $.type(o)==='date';};Typ.isBool=function(o){return $.type(o)==='boolean';};Typ.isArray=function(o){return $.type(o)=='array';};Typ.isNode=function(o){return typeof Node==="object"?o instanceof Node:o&&typeof o==="object"&&typeof o.nodeType==="number"&&typeof o.nodeName==="string";};Typ.isElement=function(o){return typeof HTMLElement==="object"?o instanceof HTMLElement:o&&typeof o==="object"&&o!==null&&o.nodeType===1&&typeof o.nodeName==="string";};Typ.isAjaxCommand=function(o){return!!(o!=undefined&&o!=false&&!Typ.isStr(o)&&o.isAjaxCommand&&o.options!=undefined&&o.displayMethod!=undefined&&o.command!=undefined);};}(typeof window!=='undefined'?window:this,jQuery,JU.__JU.Typ));(function(global,$,Arr){"use strict";Arr.isArray=function(o){if(Array.isArray){return Array.isArray(o);}
return $.type(o)=='array';};Arr.isProp=function(arr,prop){return arr.hasOwnProperty(prop);};Arr.each=function(arr,func){var i=0,k,r;for(k in arr){if(arr.hasOwnProperty(k)){r=func.call(arr,arr[k],k,i);if(r===false){break;}
i++;}}};Arr.eachJq=function(jqObj,func){var i,r,len;if(jqObj==undefined||!(jqObj instanceof jQuery)){return null;}
for(i=0,len=jqObj.length;i<len;i++){r=func.call(jqObj,jqObj.eq(i),jqObj.get(i),i);if(r===false){break;}}};Arr.range=function(start,end,step){if(end==undefined){end=start;start=0;}
if(step==undefined){step=1;}
var arr=[],val=start;while(val<end){arr.push(val);val+=step;}
return arr;};Arr.implode=function(arr,glue){glue=glue==undefined?', ':glue;return arr.join(glue);};Arr.chop=function(arr,chunkSize){var result=[],chunk;while(arr.length){chunk=arr.splice(0,chunkSize);result.push(chunk);}
return result;};Arr.chunks=function(arr,chunkSize){var result=[];for(var i=0,len=arr.length;i<len;i+=chunkSize)
result.push(arr.slice(i,i+chunkSize));return result;}}(typeof window!=='undefined'?window:this,jQuery,JU.__JU.Arr));(function(global,$,Fn){"use strict";Fn.call=function(func,thisArg,argArray){var args=[].slice.call(arguments).splice(2);return Fn.apply(func,thisArg,args);};Fn.apply=function(func,thisArg,argArray){if(func!=undefined&&$.type(func)==='function'){if(argArray==undefined){argArray=[];}
else if($.type(argArray)!='array'){argArray=[argArray];}
return func.apply(thisArg,argArray);}};Fn.callByName=function(funcName,context,argArray){if(funcName==undefined||!funcName){return;}
context=context||global;var args=[].slice.call(arguments).splice(2),namespaces=funcName.split("."),func=namespaces.pop(),i;for(i=0;i<namespaces.length;i++){context=context[namespaces[i]];if(context==undefined){return;}}
if(context[func]&&$.isFunction(context[func])){return context[func].apply(context,args);}};Fn.applyByName=function(funcName,context,argArray){if(funcName==undefined||!funcName){return;}
context=context||global;var namespaces=funcName.split("."),func=namespaces.pop(),i;for(i=0;i<namespaces.length;i++){context=context[namespaces[i]];if(context==undefined){return;}}
if(context[func]&&$.isFunction(context[func])){return context[func].apply(context,argArray);}};Fn.chain=function(thisArg,arrArray,args){var f;args=Array.prototype.splice.call(arguments,2);for(f in args){if(args.hasOwnProperty(f)){if(f!=undefined&&$.type(f)==='function'){f.apply(thisArg,arrArray);}}}};}(typeof window!=='undefined'?window:this,jQuery,JU.__JU.Fn));(function(global,$,Stl){"use strict";Stl.add=function(style){if($.isArray(style))
{$.each(style,function(i,elm){$('<link href="">').attr('href',elm).appendTo('head');});}
else if($.type(style)==='string')
{if(style.indexOf('http')==0)
{Stl.add([style]);}
else
{$('<style type="text/css">'+style+'</style>').appendTo('head');}}};}(typeof window!=='undefined'?window:this,jQuery,JU.__JU.Stl));(function(global,Str){"use strict";function _isArray(obj){return Object.prototype.toString.call(obj)==='[object Array]';}
function _parseJson(s){var _parser;if(typeof global.JSON!=='undefined'){_parser=global.JSON.parse;}
else if(typeof window.jQuery!=='undefined'){_parser=window.jQuery.parseJSON;}
if(typeof _parser==='undefined'){throw'Undefined JSON method';}
return _parser(s);}
Str.empty=function(s){return!!(s==undefined||s.length===0||Str.trim(s).length===0||!s);};Str.equals=function(s1,s2,caseSensitive){if(s1==undefined||s2==undefined){return false;}
if(caseSensitive){return s1==s2;}
return s1.toLowerCase()==s2.toLowerCase();};Str.boolVal=function(s){if(Str.empty(s)){return false;}
s=Str.trim(s).toLowerCase();if(s=='0'||s=='0.0'||s=='false'){return false;}
return!!s;};Str.regexEscape=function(s){if(!s){return'';}
if(typeof s==='string'){return s.replace(/([.?*+\^$\[\]\\(){}|\-])/g,'\\$1');}
else if(_isArray(s)){var result=[],i;for(i=0;i<s.length;i++){result.push(Str.regexEscape(s[i]));}
return result;}
return s;};Str.startsWith=function(s,pattern,caseSensitive){if(caseSensitive){return s.indexOf(pattern)===0;}
return s.toLowerCase().indexOf(pattern.toLowerCase())===0;};Str.endsWith=function(s,pattern,caseSensitive){var d=s.length-pattern.length;if(caseSensitive){return d>=0&&s.lastIndexOf(pattern)===d;}
return d>=0&&s.toLowerCase().lastIndexOf(pattern.toLowerCase())===d;};Str.contains=function(s,needle,caseSensitive){if(Str.empty(s)||Str.empty(needle)){return false;}
if(caseSensitive){return s.indexOf(needle)>-1;}
return s.toLowerCase().indexOf(needle.toLowerCase())>-1;};Str.containsAll=function(s,needles,caseSensitive){var i=0;if(_isArray(needles)){for(i=0;i<needles.length;i++){if(!Str.contains(s,needles[i],caseSensitive)){return false;}}
return true;}
return Str.contains(s,needles,caseSensitive);};Str.containsAny=function(s,needles,caseSensitive){var i;if(_isArray(needles)){for(i=0;i<needles.length;i++){if(Str.contains(s,needles[i],caseSensitive)){return true;}}
return false;}
return Str.contains(s,needles,caseSensitive);};Str.isString=function(o){return typeof o==='string';};Str.trim=function(s,c){if(!Str.isString(s)){return s;}
if(c==undefined||c==' '){if(String.prototype.trim){return String.prototype.trim.call(s);}
return s.replace(/^\s+/,'').replace(/\s+$/,'');}
return Str.trimStart(Str.trimEnd(s,c),c);};Str.trimStart=function(s,c){if(c==undefined||c==''){return s.replace(/^\s+/,'');}
var trims=c,regex,result;if(!_isArray(c)){trims=[c];}
trims=Str.regexEscape(trims).join('|');regex='^('+trims+'|\s)+';regex=new RegExp(regex,'g');result=s.replace(regex,'');return result;};Str.trimEnd=function(s,c){if(c==undefined){return s.replace(/\s+$/,'');}
var trims=c,regex,result;if(!_isArray(c)){trims=[c];}
trims=Str.regexEscape(trims).join('|');regex='('+trims+'|\s)+$';regex=new RegExp(regex,'g');result=s.replace(regex,'');return result;};Str.subStr=function(s,index,len){if(s==undefined){return'';}
len=len||0;if(Math.abs(index)>s.length){return s;}
if(index>-1){if(len>0&&(index+len)<s.length){return s.substring(index,index+len);}
return s.substring(index);}
var start=s.length+index;if(len>0&&(start+len)<s.length){return s.substring(start,start+len);}
return s.substring(start);};Str.subCount=function(s,sub,caseSensitive){sub=Str.regexEscape(sub);if(caseSensitive){return s.split(sub).length-1;}
return s.toLowerCase().split(sub.toLowerCase()).length-1;};Str.repeat=function(s,count){var result='',i;for(i=0;i<count;i++){result+=s;}
return result;};Str.padLeft=function(s,padStr,totalLength){return s.length>=totalLength?s:Str.repeat(padStr,(totalLength-s.length)/padStr.length)+s;};Str.padRight=function(s,padStr,totalLength){return s.length>=totalLength?s:s+Str.repeat(padStr,(totalLength-s.length)/padStr.length);};Str.pad=function(s,padStr,totalLength,padRight){if(padRight){return Str.padRight(s,padStr,totalLength);}
return Str.padLeft(s,padStr,totalLength);};Str.stripTags=function(s){return s.replace(/<\/?[^>]+>/gi,'');};Str.escapeHTML=function(s){s=s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');return s;};Str.unescapeHTML=function(s){return Str.stripTags(s).replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>');};Str.stripViet=function(s){if(Str.empty(s)){return s;}
s=s.replace(/[\u00E0\u00E1\u00E2\u00E3\u0103\u1EA1\u1EA3\u1EA5\u1EA7\u1EA9\u1EAB\u1EAD\u1EAF\u1EB1\u1EB3\u1EB5\u1EB7]/g,'a');s=s.replace(/[\u00F2\u00F3\u00F4\u00F5\u01A1\u1ECD\u1ECF\u1ED1\u1ED3\u1ED5\u1ED7\u1ED9\u1EDB\u1EDD\u1EDF\u1EE1\u1EE3]/g,'o');s=s.replace(/[\u00E8\u00E9\u00EA\u1EB9\u1EBB\u1EBD\u1EBF\u1EC1\u1EC3\u1EC5\u1EC7]/g,'e');s=s.replace(/[\u00F9\u00FA\u0169\u01B0\u1EE5\u1EE7\u1EE9\u1EEB\u1EED\u1EEF\u1EF1]/g,'u');s=s.replace(/[\u00EC\u00ED\u0129\u1EC9\u1ECB]/g,'i');s=s.replace(/[\u00FD\u1EF3\u1EF5\u1EF7\u1EF9]/g,'y');s=s.replace(/[\u0111\u00F0\u0110]/g,'d');return s;};Str.multiLines=function(glue,args){args=Array.prototype.splice.call(arguments,1);return args.join(glue);};Str.parseJson=function(s,defaultValue){defaultValue=defaultValue===undefined?false:defaultValue;if(Str.empty(s)){return defaultValue;}
try{if(typeof s==='string'){return _parseJson(s);}
return s;}
catch(err){return defaultValue;}};Str.escapeAttribute=function(s){return s.replace(/"/g,'\\"');};Str.reverse=function(s){if(s){return s.split('').reverse().join('');}
return s;};Str.matchAll=function(s,regex,index){var m,result=[];index=index||0;if(!s){return[];}
while(m=regex.exec(s)){result.push(m[index]);}
return result;};Str.chop=function(s,chunkSize){var regex;if(!s){return[];}
regex=new RegExp('.{1,'+chunkSize+'}','g');return s.match(regex);};function _getWords(s){s=s.replace(/(\w)([A-Z][a-z])/,'$1-$2');s=s.replace(' ','-');s=s.replace('_','-');s=s.replace(/-+/g,'-');return s.split('-')}
Str.toCamelCase=function(s){var words=_getWords(s),result='',i,word;for(i=0;i<words.length;i++){word=words[i];if(i==0){result+=word.toLowerCase();}
else{result+=word.charAt(0).toUpperCase()+word.substr(1).toLowerCase();}}
return result;};Str.toTitleCase=function(s){var words=_getWords(s),result='',i,word;for(i=0;i<words.length;i++){word=words[i];result+=word.charAt(0).toUpperCase()+word.substr(1).toLowerCase()+' ';}
return Str.trimEnd(result);};Str.toSnakeCase=function(s){var words=_getWords(s),result='',i,word;for(i=0;i<words.length;i++){word=words[i];result+=word.toLowerCase()+'_';}
return Str.trimEnd(result,'_');};Str.toKebabCase=function(s){var words=_getWords(s),result='',i,word;for(i=0;i<words.length;i++){word=words[i];result+=word.toLowerCase()+'-';}
return Str.trimEnd(result,'-');};}(typeof window!=='undefined'?window:this,JU.__JU.Str));(function(global,Utl,Str){"use strict";function _isArray(obj){return Object.prototype.toString.call(obj)==='[object Array]';}
function _isPositiveNumber(num){if(typeof num=='number'||typeof num=='string'){var number=Number(num);return isNaN(number)?false:number>=0;}
return false;}
Utl.getAttr=function(obj,attr,defaultValue){var attrParts,i,newObj,curAttr;if(obj&&attr!=undefined&&attr.length>0){if(attr.indexOf('.')==-1){if(obj.hasOwnProperty(attr)){return obj[attr];}
return defaultValue;}
else{attrParts=attr.split('.');newObj=obj;for(i=0;i<attrParts.length;i++)
{curAttr=attrParts[i];if(newObj.hasOwnProperty(curAttr)){newObj=newObj[curAttr];if(i==attrParts.length-1){return newObj;}}
else{return defaultValue;}}}}
return defaultValue;};Utl.setAttr=function(obj,attr,value,skipIfExist){var attrParts,i,newObj,arrIndex,curAttr;attr=attr==undefined?'':attr.toString();if(obj&&attr.length>0){if(attr.indexOf('.')==-1){if(!skipIfExist||!obj.hasOwnProperty(attr)){if(_isArray(obj))
{if(_isPositiveNumber(attr)){arrIndex=Number(attr);if(arrIndex>=obj.length&&arrIndex>0)
{for(i=obj.length;i<arrIndex;i++){obj.push(null);}
obj.push(value);return true;}
obj.splice(arrIndex,1,value);return true;}}
else{obj[attr]=value;return true;}}}
else{attrParts=attr.split('.');newObj=obj;for(i=0;i<attrParts.length;i++)
{curAttr=attrParts[i];if(i<attrParts.length-1){Utl.setAttr(newObj,curAttr,{},true);}
else{return Utl.setAttr(newObj,curAttr,value,skipIfExist);}
newObj=Utl.getAttr(newObj,curAttr,undefined);}}}
return false;};Utl.getPrefixedOptions=function(obj,prefix,defaultOptions){var opts={};$.each(obj,function(key,value){if(Str.startsWith(key,prefix)){opts[Str.toCamelCase(key.replace(prefix,''))]=value;}});return $.extend({},defaultOptions||{},opts)};}(typeof window!=='undefined'?window:this,JU.__JU.Utl,JU.__JU.Str));(function(global,$,Slct,Str){"use strict";Slct.getSelectedValues=function(selectElement){var $selectBox=$(selectElement),$selected=$selectBox.find('option:selected'),result=[],$firstOpt;if($selectBox.is('[multiple]')){$selected.each(function(index,element){result.push(element.value);});return result;}
$firstOpt=$selected.first();if($firstOpt.length){return $firstOpt.val();}
return null;};function _createOptions(options){var $options=$('<select multiple="multiple"></select>');$.each(options,function(index,opt){var $optGroup,$newOpt;if(opt.hasOwnProperty('optGroup')){$optGroup=$('<optgroup></optgroup>').attr('label',opt.label);if(opt.id!=undefined){$optGroup.attr('id',opt.id);}
if(opt.options!=undefined&&opt.options.length){$optGroup.append(_createOptions(opt.options));}
$options.append($optGroup);return;}
$newOpt=$('<option></option>').attr('value',opt.value).text(opt.name);if(opt.id!=undefined){$newOpt.attr('id',opt.id);}
if(opt.selected===true){$newOpt.attr('selected','selected');}
$options.append($newOpt);});return $options.children();}
Slct.addOptions=function(selectElement,options){var $selectElement=$(selectElement),$options=_createOptions(options);$selectElement.append($options);};function _getOption(selectElement,input,byValue,caseSensitive){var result=false;$(selectElement).find('option').each(function(i,option){var $option=$(option);if(byValue){if(Str.equals($option.val(),input,caseSensitive)){result=$option;return false;}}
else{if(Str.equals($option.text(),input,caseSensitive)){result=$option;return false;}}});return result;}
Slct.getOptionByValue=function(selectElement,value,caseSensitive){return _getOption(selectElement,value,true,caseSensitive);};Slct.getOptionByText=function(selectElement,text,caseSensitive){return _getOption(selectElement,text,false,caseSensitive);};Slct.removeByValue=function(selectElement,value,caseSensitive){var $option=Slct.getOptionByValue(selectElement,value,caseSensitive);if($option){$option.remove();}};Slct.removeByText=function(selectElement,text,caseSensitive){var $option=Slct.getOptionByText(selectElement,text,caseSensitive);if($option){$option.remove();}};Slct.selectByValue=function(selectElement,value,caseSensitive){var $option=Slct.getOptionByValue(selectElement,value,caseSensitive);if($option){$option.prop('selected',true);return true;}
return false;};Slct.selectByText=function(selectElement,text,caseSensitive){var $option=Slct.getOptionByText(selectElement,text,caseSensitive);if($option){$option.prop('selected',true);return true;}
return false;};Slct.selectAll=function(selectElement){$(selectElement).find('option').prop('selected',true);};Slct.selectNone=function(selectElement){$(selectElement).find('option').prop('selected',false);};Slct.isEmpty=function(selectElement){return!$(selectElement).find('option').length;};}(typeof window!=='undefined'?window:this,jQuery,JU.__JU.Slct,JU.__JU.Str));(function(global,$,Str){"use strict";Str.toHex=function(s){var r='',i;for(i=0;i<s.length;i++){r+=s.charCodeAt(i).toString(16);}
return r;};Str.fromHex=function(hex){var r='',i;for(i=0;i<hex.length;i+=2){r+=String.fromCharCode(parseInt(hex.substr(i,2),16));}
return r;};Str.format=function(s,args){args=Array.prototype.splice.call(arguments,1);s=s.replace(/\{(\d+)(:([^}]+?))?}/g,function(match,index,format,style){if(index<args.length&&args[index]!=undefined){if(!format){return args[index];}
return Str.formatObject(args[index],style);}
return match;});s=s.replace(/\{(\d+)\.([a-zA-Z0-9_]+)(:([^}]+?))?}/g,function(match,index,key,format,style){if(index<args.length&&args[index]!=undefined&&args[index].hasOwnProperty(key)){if(!format){return args[index][key];}
return Str.formatObject(args[index][key],style);}
return match;});return s;};Str.formatObject=function(o,format){if(o==undefined){return'';}
if(Dt.isValid(o)){return Dt.format(o,format);}
return o.toString();};}(typeof window!=='undefined'?window:this,jQuery,JU.__JU.Str));(function(global,$,Pref,Str){"use strict";var _defaultOptions={expires:90,path:'/',secure:false};Pref.set=function(name,value,options){var opt=$.extend({},_defaultOptions,options);if(value==undefined){$.removeCookie(name,opt);}
else{$.cookie(name,value,opt);}};Pref.get=function(name,defaultValue){var value=$.cookie(name);return value==undefined?defaultValue:value;};Pref.remove=function(name,options){var opt=$.extend({},_defaultOptions,options);$.removeCookie(name,opt);};}(typeof window!=='undefined'?window:this,jQuery,JU.__JU.Pref,JU.__JU.Str));(function(global,$,UI){"use strict";UI.lightOverlayCSS={background:'#eee url(/static/lazifier/images/ajax-loader.gif) no-repeat center',backgroundSize:'16px 16px',opacity:0.5};UI.darkOverlayCSS={background:'#000 url(/static/lazifier/images/ajax-loader.gif) no-repeat center',backgroundSize:'16px 16px',opacity:0.6};UI.defaultBlockOpts={message:null,overlayCSS:UI.lightOverlayCSS};function _prepBlockUIOptions(options){if($.type(options)==='string'){options={message:options};}
options=$.extend({},UI.defaultBlockOpts,options);return options;}
UI.block=function(elm,options){if(elm==null){return;}
options=_prepBlockUIOptions(options);if(elm==undefined){return $.blockUI(options);}
return $(elm).block(options);};UI.unblock=function(elm){if(elm==null){return;}
if(elm==undefined){return $.unblockUI();}
return $(elm).unblock();};UI.delayBlock=function(delay,elm,options){if(elm==null){return;}
return setTimeout(function(){UI.block(elm,options);},delay);};UI.delayUnblock=function(timer,elm){if(elm==null){return;}
clearTimeout(timer);UI.unblock(elm);};}(typeof window!=='undefined'?window:this,jQuery,JU.__JU.UI));(function(global,$,Patterns,UI,Str,Bs,Fn,Utl,Obj){"use strict";Patterns.formAutoFocus=function(rootElement){var $rootElement=$(rootElement),reqInput=$rootElement.find('.has-error').find('[type="text"], [type="password"], [type="email"], textarea'),input;if(reqInput.length){reqInput.first().focus().caretToEnd();}
else{input=$rootElement.find('input[type="text"], input[type="password"], textarea');if(input.length){input.first().focus().caretToEnd();}}};Patterns.submitForm=function(formSelector,targetSelector,ajaxOptions,response,parentDialog,blockOptions,context,localTarget){var $frm=$(formSelector),defaultAjaxOptions,ajaxFormOpts,userBeforeSubmit,userSuccessFunc;if(!Patterns.dependencyCheck('ajaxForm',gettext('UI.Patterns.submitForm Error'),gettext('This function requires jQuery Form (https://github.com/malsup/form.git).'))){return;}
targetSelector=targetSelector||formSelector;function setupFormSubmit()
{function removeTempHiddenFields()
{setTimeout(function(){$frm.find('input[type="hidden"][name="submit-via"]').remove();},2000);}
$frm.ajaxForm(ajaxFormOpts);$frm.find('.ajax-reset').click(function(){$frm.attr('novalidate','novalidate');$frm.append(Str.format('<input type="hidden" name="submit-via" value="{0}" />',this.name||this.value));if(!$(this).is(':submit')){$frm.submit();}
removeTempHiddenFields();});$frm.find('[type="submit"]').not('.ajax-reset').click(function(){$frm.append(Str.format('<input type="hidden" name="submit-via" value="{0}" />',this.name||this.value));removeTempHiddenFields();});}
function parseData(data)
{var newAjaxContent,result=Str.parseJson(data,false),$result,$localTarget=$(targetSelector),$fileInput;if(result===false){$result=$('<div></div>').append(data);newAjaxContent=$result.find(targetSelector);if(localTarget!=undefined){$localTarget=$(localTarget);}
$fileInput=$localTarget.find('input[type="file"]').detach();$localTarget.replaceWith(newAjaxContent);if($fileInput.length){$localTarget=$(formSelector);Arr.eachJq($fileInput,function($fileFieldWithAttachment){if($fileFieldWithAttachment.val()){var fieldName=$fileFieldWithAttachment.attr('name'),$newFileField=$localTarget.find('input[type="file"][name="'+fieldName+'"]');$newFileField.replaceWith($fileFieldWithAttachment);}});}
$frm=$(formSelector);setupFormSubmit();Patterns.formAutoFocus($frm);Fn.apply(response,this,[data]);}
else{Patterns.parseAjaxCommand(result,targetSelector,context);Fn.apply(response,this,[result]);if(parentDialog){parentDialog.close();}}}
userBeforeSubmit=ajaxOptions!=undefined&&ajaxOptions.hasOwnProperty('beforeSubmit')?ajaxOptions.beforeSubmit:undefined;userSuccessFunc=ajaxOptions!=undefined&&ajaxOptions.hasOwnProperty('success')?ajaxOptions.success:undefined;defaultAjaxOptions={dataType:'html',error:function(jqXHR,textStatus,errorThrown){UI.unblock(targetSelector);BootstrapDialog.show({title:gettext('$.ajaxForm() Error'),message:errorThrown||gettext('Error occurred while retrieving the form.'),animate:false});}};ajaxFormOpts=$.extend({},defaultAjaxOptions,ajaxOptions,{beforeSubmit:function(){Fn.apply(userBeforeSubmit,this,arguments);UI.block(targetSelector,blockOptions);},success:function(data,textStatus,jqXHR){UI.unblock(targetSelector);parseData(data);Fn.apply(userSuccessFunc,this,arguments);}});setupFormSubmit();};Patterns.ajaxRefresh=function(localTarget,remoteTarget,blockTarget,onAjaxSuccess,blockOptions){remoteTarget=remoteTarget||localTarget;blockTarget=blockTarget===undefined?localTarget:blockTarget;var ajaxCommand={isAjaxCommand:true,message:'',displayMethod:'',command:'ajax-refresh',status:'',options:{localTarget:localTarget,remoteTarget:remoteTarget},onAjaxSuccess:'onAjaxSuccess'},context={onAjaxSuccess:onAjaxSuccess};if(blockOptions)
{ajaxCommand.options=$.extend({},blockOptions,ajaxCommand.options);}
Patterns.parseAjaxCommand(ajaxCommand,blockTarget,context);};function remoteFetch(command,url,data,localTarget,remoteTarget,blockTarget,onAjaxSuccess,blockOptions){remoteTarget=remoteTarget||localTarget;blockTarget=blockTarget===undefined?localTarget:blockTarget;var ajaxCommand={isAjaxCommand:true,message:'',displayMethod:'',command:command,status:'',options:{remoteUrl:url,data:data,localTarget:localTarget,remoteTarget:remoteTarget},onAjaxSuccess:'onAjaxSuccess'},context={onAjaxSuccess:onAjaxSuccess};if(blockOptions)
{ajaxCommand.options=$.extend({},blockOptions,ajaxCommand.options);}
Patterns.parseAjaxCommand(ajaxCommand,blockTarget,context);}
Patterns.ajaxGet=function(url,data,localTarget,remoteTarget,blockTarget,onAjaxSuccess,blockOptions){remoteFetch('ajax-get',url,data,localTarget,remoteTarget,blockTarget,onAjaxSuccess,blockOptions);};Patterns.ajaxPost=function(url,data,localTarget,remoteTarget,blockTarget,onAjaxSuccess,blockOptions){remoteFetch('ajax-post',url,data,localTarget,remoteTarget,blockTarget,onAjaxSuccess,blockOptions);};Patterns.parseAjaxCommand=function(ajaxCommand,blockTarget,context)
{if($.type(ajaxCommand)==='string'){ajaxCommand=Str.parseJson(ajaxCommand,false);}
if(!Typ.isAjaxCommand(ajaxCommand)){return false;}
if(ajaxCommand.command=='ajax-refresh'){ajaxCommand.command='ajax-get';ajaxCommand.options.remoteUrl='';if(ajaxCommand.options.commonTarget){ajaxCommand.options.localTarget=ajaxCommand.options.commonTarget;ajaxCommand.options.remoteTarget=ajaxCommand.options.commonTarget;delete ajaxCommand.options.commonTarget;}}
var defaultBlockUiOptions,blockOptions,bsDialogOpts,defaultBsDialogOpts,toastrOpts,defaultToastrOpts,toastrType,toastrTitle,displayMethod=ajaxCommand.displayMethod,command=ajaxCommand.command,options=ajaxCommand.options,hasSyncAction,canDisplayAsyncTask=false;hasSyncAction=$.inArray(ajaxCommand.command,['refresh','redirect'])!=-1;blockTarget=blockTarget===undefined?options.localTarget:blockTarget;if(Fn.callByName(ajaxCommand.onPreParse,context,options,ajaxCommand)===false)
{Fn.callByName(ajaxCommand.onPostParse,context,options,ajaxCommand);return;}
function executeSyncActions()
{var htmlContent=ajaxCommand.options.htmlContent;if(htmlContent&&ajaxCommand.options.contentSelector){htmlContent=$('<div></div>').append(htmlContent).find(ajaxCommand.options.contentSelector);}
if(command=='ajax-get'||command=='ajax-post'){UI.block(blockTarget);setTimeout(function(){canDisplayAsyncTask=true;},500);}
if(command=='refresh'){global.location.reload(true);}
else if(command=='redirect'){global.location=ajaxCommand.options.redirectUrl;}
else if(command=='replace-html'){$(ajaxCommand.options.localTarget).replaceWith(htmlContent);}
else if(command=='append-html'){$(ajaxCommand.options.localTarget).append(htmlContent);}
else if(!Str.empty(ajaxCommand.onPostParse)){Fn.callByName(ajaxCommand.onPostParse,context,options,ajaxCommand);}}
function executeAsyncActions(){var asyncTaskTimer,ajaxOptions;function displayAsyncTask(content,isError){return setInterval(function(){if(canDisplayAsyncTask){clearInterval(asyncTaskTimer);UI.unblock(blockTarget);var $result=$('<div></div>').append(content),$localTarget;if(!Str.empty(options.remoteTarget)){$result=$result.find(options.remoteTarget);}
$localTarget=$(options.localTarget);if(isError){$localTarget.empty().append(content);}
else{$localTarget.replaceWith($result);if(!Str.empty(ajaxCommand.onAjaxSuccess)){Fn.callByName(ajaxCommand.onAjaxSuccess,context,content,ajaxCommand);}}}},100);}
if(command=='ajax-get'||command=='ajax-post'){ajaxOptions={url:options.remoteUrl||'',method:command=='ajax-post'?'POST':'GET',data:options.data||''};$.ajax(ajaxOptions).done(function(data){asyncTaskTimer=displayAsyncTask(data,false);}).fail(function(jqXHR,textStatus,errorThrown){var errorMsg=gettext(errorThrown);if(errorMsg){errorMsg=Str.format('Error: {0}',errorMsg);}
else{errorMsg=gettext('Errors occurred while retrieving data from the server ...');}
asyncTaskTimer=displayAsyncTask(errorMsg,true);});}}
if(displayMethod=='block-ui')
{defaultBlockUiOptions={message:ajaxCommand.message||null,blockTarget:blockTarget,delay:hasSyncAction?300:2000};blockOptions=Utl.getPrefixedOptions(options,'blockUi',defaultBlockUiOptions);UI.block(blockOptions.blockTarget,blockOptions);executeAsyncActions();setTimeout(function(){executeSyncActions();if(!hasSyncAction){UI.unblock(blockOptions.blockTarget);}},blockOptions.delay);}
else if(displayMethod=='bs-dialog')
{defaultBsDialogOpts={title:options.title||gettext('Message'),message:ajaxCommand.message,animate:false,type:ajaxCommand.status=='error'?'type-danger':'type-primary',buttons:[{label:gettext('OK'),cssClass:'btn-primary',action:function(dialog){dialog.close();}}],onhidden:function(){executeSyncActions();}};executeAsyncActions();bsDialogOpts=Utl.getPrefixedOptions(options,'bsDialog',defaultBsDialogOpts);BootstrapDialog.show(bsDialogOpts);}
else if(displayMethod=='toastr')
{if(!Patterns.dependencyCheck(global.toastr,gettext('UI.Patterns.parseAjaxCommand Toastr Error'),gettext('This function requires toastr plugins (https://github.com/CodeSeven/toastr).'))){return;}
defaultToastrOpts={title:undefined,type:ajaxCommand.status=='error'?'error':'success',closeButton:true,newestOnTop:true,positionClass:'toast-top-right',onHidden:function(){executeSyncActions();}};executeAsyncActions();toastrOpts=Utl.getPrefixedOptions(options,'toastr',defaultToastrOpts);toastrType=Obj.pop(toastrOpts,'type','success');toastrTitle=Obj.pop(toastrOpts,'title',undefined);toastr[toastrType](ajaxCommand.message,toastrTitle,toastrOpts)}
else if(displayMethod=='alert'){executeAsyncActions();alert(ajaxCommand.message);executeSyncActions();}
else{executeAsyncActions();executeSyncActions();}
return ajaxCommand;};Patterns.bsDialogAjax=function(title,ajaxOpts,dialogOptions,shown,hidden,context){if(global.BootstrapDialog==undefined){alert('This function required Bootstrap Dialog plugin.');return;}
var defaultOptions,options;defaultOptions={title:title,message:gettext('Loading, please wait ... '),animate:false,onshown:function($dialogRef){var uiBlockTmr,$modalDialog=$dialogRef.getModalDialog();uiBlockTmr=UI.delayBlock(300,$modalDialog);function unblockWaitingScreen(){UI.delayUnblock(uiBlockTmr,$modalDialog);}
$.ajax(ajaxOpts).done(function(data){var result=Str.parseJson(data,false);if(result===false){$modalDialog.find('.modal-body').empty().append(data);Patterns.formAutoFocus($modalDialog);Fn.apply(shown,$dialogRef,[data]);unblockWaitingScreen();}
else{unblockWaitingScreen();$dialogRef.close();UI.Patterns.parseAjaxCommand(result,$modalDialog,context);}}).fail(function(jqXHR,textStatus,errorThrown){unblockWaitingScreen();errorThrown=gettext(errorThrown)||gettext('Error occurred while retrieving the form.');$modalDialog.find('.modal-body').empty().append(Str.format('<span class="error">{0}</span>',errorThrown));});},onhidden:function(dialogRef){Fn.apply(hidden,dialogRef);}};options=$.extend({},dialogOptions,defaultOptions);return BootstrapDialog.show(options);};Patterns.submitAjaxRequest=function(ajaxOpts,blockTarget,onComplete,context){var uiBlockTmr=UI.delayBlock(300,blockTarget);function unblockWaitingScreen(){UI.delayUnblock(uiBlockTmr,blockTarget);}
$.ajax(ajaxOpts).done(function(data){var ajaxCommand=Str.parseJson(data,false);if(ajaxCommand!=false){unblockWaitingScreen();UI.Patterns.parseAjaxCommand(ajaxCommand,blockTarget,context);if(!ajaxCommand.isAjaxCommand){Fn.apply(onComplete,blockTarget||this,[ajaxCommand]);}}
else{unblockWaitingScreen();Fn.apply(onComplete,blockTarget||this,[data]);}}).fail(function(jqXHR,textStatus,errorThrown){unblockWaitingScreen();BootstrapDialog.show({title:gettext('Error'),animate:false,message:gettext(errorThrown)||gettext('Error occurred while submitting ...')});});};var cache_selectAjaxFilter={};Patterns.selectAjaxFilter=function(srcSelect,targetSelect,ajaxOpts,targetUpdated,noCache,container){ajaxOpts=$.type(ajaxOpts)==='string'?{url:ajaxOpts}:ajaxOpts;var $container=$(container||'body');$container.on('change',srcSelect,function(){var $srcSelect=$container.find(srcSelect),$targetSelect=$container.find(targetSelect),selectedValues=Slct.getSelectedValues($srcSelect),errorMessage=gettext('Error occurred while retrieving data from the server.'),opt={data:{src_name:$srcSelect.attr('name'),target_name:$targetSelect.attr('name')}},token=$.cookie('csrftoken'),cacheKey;if(Typ.isArray(selectedValues)){cacheKey=$srcSelect.attr('name')+'_'+Arr.implode(selectedValues,'|');}
else{cacheKey=$srcSelect.attr('name')+'_'+selectedValues;}
opt.data[$srcSelect.attr('name')]=selectedValues;opt=$.extend({},ajaxOpts,opt);if(token!=undefined&&opt.data.csrfmiddlewaretoken==undefined&&token!=undefined){opt.data.csrfmiddlewaretoken=token;}
function loadOptions(options){if(Typ.isJquery(options)){$targetSelect.empty().append(options);}
else
{$targetSelect.empty();Slct.addOptions($targetSelect,options);}
Fn.apply(targetUpdated,$targetSelect.get(0),[$targetSelect]);}
if(!noCache&&cache_selectAjaxFilter.hasOwnProperty(cacheKey))
{loadOptions(cache_selectAjaxFilter[cacheKey]);return;}
$.ajax(opt).done(function(data){var options=Str.parseJson(data,false),targetId,targetName,selector,$options,$data;if(options!==false){cache_selectAjaxFilter[cacheKey]=options;loadOptions(options);}
else{$data=$(data);targetId=$targetSelect.attr('id');if(targetId){selector='select#'+targetId;$options=$data.find(selector);}
targetName=$targetSelect.attr('name');if(targetName&&!$options.length){selector='select[name="'+targetName+'"]';$options=$data.find(selector);}
if($options.length){cache_selectAjaxFilter[cacheKey]=$options.children();loadOptions($options.children());}
else{BootstrapDialog.alert(errorMessage);}}}).fail(function(jqXHR,textStatus,errorThrown){BootstrapDialog.show({title:errorThrown,animate:false,message:errorMessage});});});if(!Slct.getSelectedValues($(targetSelect))){$(srcSelect).change();}};Patterns.clearOnEscape=function(inputSelector,container){var $container=$(container),$input=$(inputSelector),$target;function clearOnEscape(e){if(e.which==27){$target=$(e.target);$target.prop('value',null).val('').change();}}
if(container&&$container.length){$container.on('keyup',inputSelector,clearOnEscape);}
else{$input.on('keyup',clearOnEscape);}};Patterns.dependencyCheck=function(testObj,title,message){var result=false;if(testObj){if($.type(testObj)=='string'){result=$.fn.hasOwnProperty(testObj);}
else{result=true;}}
if(result){return true;}
if($.fn.hasOwnProperty('ajaxForm')){BootstrapDialog.show({title:title,message:message,animate:false});}
else if(global.toastr!=undefined){global.toastr.error(message,title);}
else{alert(title+"\n"+message);}
return false;};}(typeof window!=='undefined'?window:this,jQuery,JU.__JU.UI.Patterns,JU.__JU.UI,JU.__JU.Str,JU.__JU.Bs,JU.__JU.Fn,JU.__JU.Utl,JU.__JU.Obj));(function(global,$,Bs){"use strict";Bs.confirmYesNo=function(message,buttonClicked){function invokeButtonClicked(dialog,result){if(buttonClicked!=undefined){Fn.apply(buttonClicked,dialog,[result]);buttonClicked=null;dialog.close();}}
BootstrapDialog.show({title:gettext('Confirmation'),message:message,animate:false,buttons:[{label:gettext('(N) No'),hotkey:78,action:function(dialog){invokeButtonClicked(dialog,false);}},{label:gettext('(Y) Yes'),hotkey:89,cssClass:'btn-primary',action:function(dialog){invokeButtonClicked(dialog,true);}}],onhide:function(dialog){invokeButtonClicked(dialog,false);}});};}(typeof window!=='undefined'?window:this,jQuery,JU.__JU.UI.Bs));(function(global){"use strict";if(!global.JU.__JU){return;}
var forcePush=false;global.JU.publish(global.JU.__JU,global.JU._autoPopulateGlobal,forcePush);delete global.JU.__JU;}(typeof window!=='undefined'?window:this));