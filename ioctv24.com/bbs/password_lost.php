<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta http-equiv="imagetoolbar" content="no">
<meta http-equiv="X-UA-Compatible" content="IE=Edge">
<meta name="title" content="회원정보 찾기 > 올림픽티비" />
<meta name="publisher" content="올림픽티비" />
<meta name="author" content="올림픽티비" />
<meta name="robots" content="index,follow" />
<meta name="keywords" content="올림픽티비" />
<meta name="description" content="회원정보 찾기 > 올림픽티비" />
<meta name="twitter:card" content="summary_large_image" />
<meta property="og:title" content="회원정보 찾기 > 올림픽티비" />
<meta property="og:site_name" content="올림픽티비" />
<meta property="og:author" content="올림픽티비" />
<meta property="og:type" content="" />
<meta property="og:description" content="회원정보 찾기 > 올림픽티비" />
<meta property="og:url" content="password_lost.php" />
<link rel="canonical" href="password_lost.php" />
<title>회원정보 찾기 > 올림픽티비</title>
<link rel="stylesheet" href="../css/default__q_ver_180827.css">
<link rel="stylesheet" href="../css/apms__q_ver_180827.css">
<link rel="stylesheet" href="../thema/tv/assets/bs3/css/bootstrap.min__q_180827.css" type="text/css">
<link rel="stylesheet" href="../thema/tv/colorset/Basic/colorset__q_180827.css" type="text/css">
<link rel="stylesheet" href="../skin/member/basic/style.css" >
<!--[if lte IE 8]>
<script src="https://ioctv24.com//js/html5.js"></script>
<![endif]-->
<script>
// 자바스크립트에서 사용하는 전역변수 선언
var g5_url       = "https://ioctv24.com/";
var g5_bbs_url   = "https://ioctv24.com//bbs";
var g5_is_member = "";
var g5_is_admin  = "";
var g5_is_mobile = "";
var g5_bo_table  = "";
var g5_sca       = "";
var g5_pim       = "";
var g5_editor    = "";
var g5_responsive    = "1";
var g5_cookie_domain = "";
var g5_purl = "password_lost.php";
</script>
<script src="../js/jquery-1.8.3.min.js"></script>
<script src="../js/jquery-migrate-1.2.1.min.js"></script>
<script src="../lang/korean/lang__q_ver_180827.js"></script>
<script src="../js/common__q_ver_180827.js"></script>
<script src="../js/wrest__q_ver_180827.js"></script>
<script src="../js/placeholders.min.js"></script>
<script src="../js/apms__q_ver_180827.js"></script>
<link rel="stylesheet" href="../js/font-awesome/css/font-awesome.min.css">
<link rel="icon" href="../img/favicon__q_v_3.png"/>  

</head>
<body class="responsive is-pc">
	<h1 style="display:inline-block !important;position:absolute;top:0;left:0;margin:0 !important;padding:0 !important;font-size:0;line-height:0;border:0 !important;overflow:hidden !important">
	회원정보 찾기 > 올림픽티비	</h1>
<div class="ko">
<form class="form-horizontal" role="form" name="fpasswordlost" action="https://ioctv24.com//bbs/password_lost2.php" onsubmit="return fpasswordlost_submit(this);" method="post" autocomplete="off">

	<div class="panel panel-default">
		<div class="panel-heading"><strong><i class="fa fa-search fa-lg"></i> 회원정보찾기</strong></div>
		<div class="panel-body">
			<p class="help-block">
				회원가입 시 등록하신 이메일 주소를 입력해 주세요. 해당 이메일로 아이디와 비밀번호 정보를 보내드립니다.
			</p>
			<div class="form-group has-feedback">
				<label class="sound_only" for="mb_email"><b>이메일</b><strong class="sound_only">필수</strong></label>
				<div class="col-xs-10">
					<input type="text" name="mb_email" id="mb_email" required class="form-control input-sm email" size="30" maxlength="100">
					<span class="fa fa-envelope form-control-feedback"></span>
				</div>
			</div>

			<div class="form-group">
				<div class="col-xs-10">
					
<script>var g5_captcha_url  = "https://ioctv24.com//plugin/kcaptcha";</script>
<script src="../plugin/kcaptcha/kcaptcha.js"></script>
<fieldset id="captcha" class="captcha">
<legend><label for="captcha_key">자동등록방지</label></legend>
<img src="../plugin/kcaptcha/img/dot.gif" alt="" id="captcha_img"><input type="text" name="captcha_key" id="captcha_key" required class="captcha_box required" size="6" maxlength="6">
<button type="button" id="captcha_mp3"><span></span>숫자음성듣기</button>
<button type="button" id="captcha_reload"><span></span>새로고침</button>
<span id="captcha_info">자동등록방지 숫자를 순서대로 입력하세요.</span>
</fieldset>				</div>
			</div>
		</div>
	</div>

	<div class="text-center" style="margin:15px 0px 0px;">
		<button type="submit" class="btn btn-color btn-sm">확인</button>
        <button type="button" class="btn btn-black btn-sm" onclick="window.close();">닫기</button>
	</div>
</form>

<script>
function fpasswordlost_submit(f) {
    if (!chk_captcha()) return false;

    return true;
}

$(function() {
    var sw = screen.width;
    var sh = screen.height;
    var cw = document.body.clientWidth;
    var ch = document.body.clientHeight;
    var top  = sh / 2 - ch / 2 - 100;
    var left = sw / 2 - cw / 2;
    moveTo(left, top);
});
</script>
<!-- } 회원정보 찾기 끝 --></div>

<!--[if lt IE 9]>
<script type="text/javascript" src="https://ioctv24.com//thema/tv/assets/js/respond.js"></script>
<![endif]-->

<!-- JavaScript -->
<script type="text/javascript" src="../thema/tv/assets/bs3/js/bootstrap.min.js"></script>
<script type="text/javascript" src="../thema/tv/assets/js/custom.sub.js"></script>
<!-- 아미나빌더 1.8.57 / 그누보드 5.3.3.3(패치 G5.6.10) -->
<script defer src="https://static.cloudflareinsights.com/beacon.min.js/v8c78df7c7c0f484497ecbca7046644da1771523124516" integrity="sha512-8DS7rgIrAmghBFwoOTujcf6D9rXvH8xm8JQ1Ja01h9QX8EzXldiszufYa4IFfKdLUKTTrnSFXLDkUEOTrZQ8Qg==" data-cf-beacon='{"version":"2024.11.0","token":"195f804a95e045d4ba58b18f86dc453e","r":1,"server_timing":{"name":{"cfCacheStatus":true,"cfEdge":true,"cfExtPri":true,"cfL4":true,"cfOrigin":true,"cfSpeedBrain":true},"location_startswith":null}}' crossorigin="anonymous"></script>
</body>
</html>
