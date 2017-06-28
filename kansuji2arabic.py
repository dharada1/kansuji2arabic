# -*- coding: utf-8 -*-
import re
import string
import sys

# 一〜九までを1〜9にreplaceして結果のstringを返す
def kansuji2num_replace(kansuji_str):
	num_replace_dict = {
		u"一":u"1",
		u"二":u"2",
		u"三":u"3",
		u"四":u"4",
		u"五":u"5",
		u"六":u"6",
		u"七":u"7",
		u"八":u"8",
		u"九":u"9"
	}

	for k,v in num_replace_dict.items():
		kansuji_str = kansuji_str.replace(k,v)
	return kansuji_str

#[兆,億,万,一]のように区切って4桁ずつの日本語漢数字が入っているnumber_list_Aを作成する。
def separate_kanji_str_into_each_four_digits(kansuji_str):
	number_list_A = []
	if (u"万" not in kansuji_str) and (u"億" not in kansuji_str) and (u"兆" not in kansuji_str):
		number_list_A = [u"0", u"0", u"0", kansuji_str]
	else:
		#[""兆 "" ""?]
		chou_div_list = kansuji_str.split(u"兆")
		if len(chou_div_list) == 1:
			number_list_A = [u"0", chou_div_list[0]]
		elif len(chou_div_list) == 2:
			number_list_A = chou_div_list

		#[""兆 ""億 ""?]
		oku_div_list = number_list_A[1].split(u"億")
		if len(oku_div_list) == 1:
			number_list_A = [number_list_A[0], u"0", oku_div_list[0]]
		elif len(oku_div_list) == 2:
			number_list_A = [number_list_A[0]] + oku_div_list

		#[""兆 ""億 ""万 ""] 完成
		man_div_list = number_list_A[2].split(u"万")
		if len(man_div_list) == 1:
			if man_div_list[0] != u"":
				number_list_A = [number_list_A[0], number_list_A[1], u"0", man_div_list[0]]
			else:
				number_list_A = [number_list_A[0], number_list_A[1], u"0", u"0"]
		elif len(man_div_list) == 2:
			if man_div_list[1] != u"":
				number_list_A = [number_list_A[0], number_list_A[1]] + man_div_list
			else:
				number_list_A = [number_list_A[0], number_list_A[1], man_div_list[0], u"0"]

	return number_list_A

# ================================================
# "千十八" => [1,0,1,8] 処理部分
# ================================================
def divide_4digit_number(kansuji_str):
	#TODO: この時点で一〜九、十百千以外が混入してたらエラー吐いて上の方でキャッチする処理にする

	number_list_C = []
	if (u"千" not in kansuji_str) and (u"百" not in kansuji_str) and (u"十" not in kansuji_str):
		#一桁の場合
		number_list_C = [u"0", u"0", u"0", kansuji_str]
	else:
		#千、百、十いずれかを含む複数桁の場合

		# 千split
		# "二千三百十二" から ["二", "三百十二"]
		sen_div_list = kansuji_str.split(u"千")
		if len(sen_div_list) == 1: #千が含まれてなかった場合右へshiftして持ち越し
			number_list_C = [u"0", sen_div_list[0]]
		elif len(sen_div_list) == 2: #千が含まれていた場合、一千の省略の千の場合/二千などの場合 と分けて処理
			if sen_div_list[0] == u"": #一千の省略の千の場合,1を追加する
				number_list_C = [u"1", sen_div_list[1]]
			else: #"二千三百十二" のとき sen_div_list = [u"二",u"三百十二"]
				number_list_C = sen_div_list

		# 百split
		# ["二", "三百十二"] から ["二", "三", "十二"]
		hyaku_div_list = number_list_C[1].split(u"百")
		if len(hyaku_div_list) == 1: #百が含まれてなかった場合右へshiftして持ち越し
			number_list_C = [number_list_C[0], u"0", hyaku_div_list[0]]
		elif len(hyaku_div_list) == 2: #百が含まれていた場合、一百の省略の百の場合/二百などの場合 と分けて処理
			if hyaku_div_list[0] == u"":
				number_list_C = [number_list_C[0], u"1", hyaku_div_list[1]]
			else:
				number_list_C = [number_list_C[0]] + hyaku_div_list

		#十split
		# ["二", "三", "十二"] から ["二", "三", "1", "二"]
		zyuu_div_list = number_list_C[2].split(u"十")
		if len(zyuu_div_list) == 1: #十が含まれていなかった場合、これが一桁目の数字なので格納
			if zyuu_div_list[0] == u"":
				number_list_C = [number_list_C[0], number_list_C[1], u"0", u"0"]
			else:
				number_list_C = [number_list_C[0], number_list_C[1], u"0", zyuu_div_list[0]]
		elif len(zyuu_div_list) == 2: #十が含まれていた場合、一十の省略の十の場合/二十などの場合 と分けて処理
			if zyuu_div_list[0] == u"": #十の場合
				if zyuu_div_list[1] == u"": #一の位が無い
					number_list_C = [number_list_C[0], number_list_C[1], u"1", u"0"]
				else: #一の位がある
					number_list_C = [number_list_C[0], number_list_C[1], u"1", zyuu_div_list[1]]
			else: #二十〜九十の場合
				if zyuu_div_list[1] == u"": #一の位が無い
					number_list_C = [number_list_C[0], number_list_C[1], zyuu_div_list[0], u"0"]
				else: #一の位がある
					number_list_C = [number_list_C[0], number_list_C[1]] + zyuu_div_list

		# # ===============================
		# # number_list_C表示部分
		# print ""
		# print "number_list_C:"
		# print number_list_C
		# print "中身:"
		# print "[",
		# for numstr in number_list_C:
		# 	if (numstr == u""):
		# 		print "バグ",
		# 	else:
		# 		print numstr + ",",
		# print "]"
		# print ""
		# # ===============================

	#number_list_Cの各要素について、漢数字を数字に置換して結果を返す。
	number_list_D = []
	for number_kanji in number_list_C:
		number = kansuji2num_replace(number_kanji)
		number_list_D.append(number)
	return number_list_D

# ==========================================================================
# [兆,億,万,一]のように区切って4桁ずつの日本語漢数字が入っているnumber_list_Aから
# 一桁1数字対応のリストに変換をして返す
# 例: 二兆十八
# [ 二, 0, 0, 十八 ] => [ 0,0,0,二, 0,0,0,0, 0,0,0,0, 0,0,一,八]
# => [ 0,0,0,2, 0,0,0,0, 0,0,0,0, 0,0,1,8]
# ==========================================================================
def separate_4digit_list_into_flat_list(number_list_A):
	# ================================================
	# number_list_Aの各要素についてflattenする
	# ================================================
	number_list_B = []
	for number_4digit_str in number_list_A:
		number_list_C = divide_4digit_number(number_4digit_str)
		number_list_B += number_list_C

	return number_list_B


# ==========================================================================
# [u'0', u'0', u'0', u'0', u'0', u'0', u'0', u'0', u'0', u'0', u'0', u'0', u'2', u'0', u'1', u'6']
# => 2016
# ==========================================================================
def number_list_to_number_str(number_list):
	#0詰めで結合する。
	#0000000000002016
	number_str = u"".join(number_list)

	#頭の0を消す。
	#2016
	number_str = re.sub('^0+', '', number_str)
	return number_str


# メイン処理
def kansuji2arabic(kansuji_str):
	#TODO: 一〜九、十百千万億兆 以外が入ってたらエラー出してエラー吐いて上の方でキャッチする処理にする

	# print 'kansuji2arabic.'.ljust( 80, '=' )

	# print "入力:", kansuji_str


	#漢数字を単純にnum_replace_dictを用いてアラビア数字に置換する部分
	#print "置換:", kansuji2num_replace(kansuji_str)

	#[兆,億,万,一]のように区切って4桁ずつの日本語漢数字が入っているnumber_list_Aを作成する。
	number_list_A = separate_kanji_str_into_each_four_digits(kansuji_str)

	# # number_list_A表示部分
	# print ""
	# print "[兆,億,万,一]で区切って4桁ずつの日本語漢数字が入っているnumber_list_A:"
	# print number_list_A
	# print "中身:"
	# print "[",
	# for numstr in number_list_A:
	# 	if (numstr == u""):
	# 		print "バグ",
	# 	else:
	# 		print numstr + ",",
	# print "]"
	# print ""


	#[ 二, 0, 0, 十八 ] => [ 0,0,0,二, 0,0,0,0, 0,0,0,0, 0,0,一,八]
	#=> [ 0,0,0,2, 0,0,0,0, 0,0,0,0, 0,0,1,8]
	number_list_B = separate_4digit_list_into_flat_list(number_list_A)

	# print "number_list_B:"
	# print number_list_B

	# print '\n'.rjust( 80, '=' )

	# number_list_Bの各桁に桁数分x10して計算する処理かませてreturnする
	return number_list_to_number_str(number_list_B)

if __name__ == '__main__':
 	argvs = sys.argv  # コマンドライン引数を格納したリストの取得
	argc = len(argvs) # 引数の個数
	if (argc == 2):
		print kansuji2arabic(argvs[1].decode('utf-8'))
	else:
		print "使用例: python kansuji2arabic.py 八兆五千二百四十七"