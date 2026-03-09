$(function(){
		var num0 = "li.num0";
		var num1 = "li.num1";
		var num2 = "li.num2";
		var num3 = "li.num3";
		var num4 = "li.num4";
		var num5 = "li.num5";
		var num6 = "li.num6";
		var num7 = "li.num7";
		var num8 = "li.num8";
		var num9 = "li.num9";

	   $(num0).mouseover(function(){
	      $("div#top_gnb ul.gnb_default ul.num0_over").css({"display":"block"});
	      $("li.num0").addClass("on");
	   });
	   $(num0).mouseout(function(){
	      $("div#top_gnb ul.gnb_default ul.num0_over").css({"display":"none"});
	      $("li.num0").removeClass("on");
	   });
	   
	   $(num6).mouseover(function(){
	      $("ul.num6_over").css({"display":"block"});
	      $("li.num6").addClass("on");
	   });
	   $(num6).mouseout(function(){
	      $("ul.num6_over").css({"display":"none"});
	      $("li.num6").removeClass("on");
	   });

	   $(num7).mouseover(function(){
	      $("ul.num7_over").css({"display":"block"});
	      $("li.num7").addClass("on");
	   });
	   $(num7).mouseout(function(){
	      $("ul.num7_over").css({"display":"none"});
	      $("li.num7").removeClass("on");
	   });

	   $(num8).mouseover(function(){
	      $("ul.num8_over").css({"display":"block"});
	      $("li.num8").addClass("on");
	   });
	   $(num8).mouseout(function(){
	      $("ul.num8_over").css({"display":"none"});
	      $("li.num8").removeClass("on");
	   });

	   $(num9).mouseover(function(){
	      $("ul.num9_over").css({"display":"block"});
	      $("li.num9").addClass("on");
	   });
	   $(num9).mouseout(function(){
	      $("ul.num9_over").css({"display":"none"});
	      $("li.num9").removeClass("on");
	   });
	   
	   $(num1).mouseover(function(){
	      $("div#top_gnb ul.gnb_default ul.num1_over").css({"display":"block"});
	      $("li.num2").addClass("on");
	   });
	   $(num1).mouseout(function(){
	      $("div#top_gnb ul.gnb_default ul.num1_over").css({"display":"none"});
	      $("li.num2").removeClass("on");
	   });
	   $(num2).mouseover(function(){
	      $("div#top_gnb ul.gnb_default ul.num2_over").css({"display":"block"});
	      $("li.num2").addClass("on");
	   });
	   $(num2).mouseout(function(){
	      $("div#top_gnb ul.gnb_default ul.num2_over").css({"display":"none"});
	      $("li.num2").removeClass("on");
	   });

	   $(num3).mouseover(function(){
	      $("div#top_gnb ul.gnb_default ul.num3_over").css({"display":"block"});
	      $("li.num3").addClass("on");
	   });
	   $(num3).mouseout(function(){
	      $("div#top_gnb ul.gnb_default ul.num3_over").css({"display":"none"});
	      $("li.num3").removeClass("on");
	   });
	   $(num4).mouseover(function(){
	      $("div#top_gnb ul.gnb_default ul.num4_over").css({"display":"block"});
	      $("li.num4").addClass("on");
	   });
	   $(num4).mouseout(function(){
	      $("div#top_gnb ul.gnb_default ul.num4_over").css({"display":"none"});
	      $("li.num4").removeClass("on");
	   });
	   $(num5).mouseover(function(){
	      $("div#top_gnb ul.gnb_default ul.num5_over").css({"display":"block"});
	      $("li.num5").addClass("on");
	   });
	   $(num5).mouseout(function(){
	      $("div#top_gnb ul.gnb_default ul.num5_over").css({"display":"none"});
	      $("li.num5").removeClass("on");
	   });
	});

$(function(){
		var tab1 = "div.tab_box div.tab_box_inner div.multi_tab ul li.free";
		var tab2 = "div.tab_box div.tab_box_inner div.multi_tab ul li.humor";
		var tab3 = "div.tab_box div.tab_box_inner div.multi_tab ul li.news";
		var tab4 = "div.tab_box div.tab_box_inner div.multi_tab ul li.ver";
		var tab5 = "div.tab_box div.tab_box_inner div.multi_tab ul li.cng";
		var tab6 = "div.tab_box div.tab_box_inner div.multi_tab ul li.hi";
		var tab7 = "input.domain_search";
	   $(tab1).click(function(){

	      $("div.free_con").css({"display":"block"});
	      $("li.free").addClass("on");
	      $("li.humor,li.news,li.ver,li.cng,li.hi").removeClass("on");
	      $("div.humor_con,div.news_con,div.ver_con,div.cng_con,div.hi_con").css({"display":"none"});
	   });

	   $(tab2).click(function(){
	      $("div.humor_con").css({"display":"block"});
	      $("li.humor").addClass("on");
	      $("li.free,li.news,li.ver,li.cng,li.hi").removeClass("on");
	      $("div.free_con,div.news_con,div.ver_con,div.cng_con,div.hi_con").css({"display":"none"});
	   });


	   $(tab3).click(function(){
	      $("div.news_con").css({"display":"block"});
	      $("li.news").addClass("on");
	      $("li.free,li.humor,li.ver,li.cng,li.hi").removeClass("on");
	      $("div.free_con,div.humor_con,div.ver_con,div.cng_con,div.hi_con").css({"display":"none"});
	   });


	   $(tab4).click(function(){
	      $("div.ver_con").css({"display":"block"});
	      $("li.ver").addClass("on");
	      $("li.free,li.news,li.humor,li.cng,li.hi").removeClass("on");
	      $("div.free_con,div.news_con,div.cng_con,div.hi_con,div.humor_con").css({"display":"none"});
	   });

	   $(tab5).click(function(){
	      $("div.cng_con").css({"display":"block"});
	      $("li.cng").addClass("on");
	      $("li.free,li.news,li.humor,li.ver,li.hi").removeClass("on");
	      $("div.free_con,div.news_con,div.ver_con,div.hi_con,div.humor_con").css({"display":"none"});
	   });
	   $(tab6).click(function(){
	      $("div.hi_con").css({"display":"block"});
	      $("li.hi").addClass("on");
	      $("li.free,li.news,li.humor,li.ver,li.cng").removeClass("on");
	      $("div.free_con,div.news_con,div.ver_con,div.cng_con,div.humor_con").css({"display":"none"});
	   });
	   $(tab7).click(function(){
	      $("div.domain_con").css({"display":"block"});
	   });
	});


$(function(){
		var tab1 = ".aside_point_ranking";
		var tab2 = "div.point_ranking div.ranking_inner span.close";
		var tab3 = ".aside_point_ranking";
	   $(tab1).click(function(){
	      $("div.point_ranking").show(200);
	   });

	   $(tab2).click(function(){
	      $("div.point_ranking").hide(200);
	   });
	});


$(function(){
		var tab_auto1 = "div.tab_box div.tab_box_inner div.multi_tab ul li.free";
		var tab_auto2 = "div.tab_box div.tab_box_inner div.multi_tab ul li.humor";
		var tab_auto3 = "div.tab_box div.tab_box_inner div.multi_tab ul li.news";
		var tab_auto4 = "div.tab_box div.tab_box_inner div.multi_tab ul li.ver";
		var tab_auto5 = "div.tab_box div.tab_box_inner div.multi_tab ul li.cng";
		var tab_auto6 = "div.tab_box div.tab_box_inner div.multi_tab ul li.hi";
});


