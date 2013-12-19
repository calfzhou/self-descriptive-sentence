#include "chinese.h"

namespace Chinese {

static std::string strChDig[] =
	{ "零","十","百","千","万","亿","兆" };
static std::string strChNum[] =
	{"零","一","二","三","四","五","六","七","八","九","十"};

std::string ChineseNumber(int i)
{
	if( i<0	) return "负" +	ChineseNumber (-i);
	if( i<11 ) return strChNum[i];
	if( i<20 ) return strChNum[10] + strChNum[i-10];
	if( i<100 ) {
		if( i%10 ) return strChNum[i/10] +	strChDig[1] + strChNum[i%10];
		else return strChNum[i/10]	+ strChDig[1];
	}
	if( i<1000 ) {
		if( i%100==0 )
			return strChNum[i/100] + strChDig[2];
		else if( i%100 < 10 )
			return strChNum[i/100] + strChDig[2] + strChNum[0] + ChineseNumber (i%100);
		else if( i%100 < 20 )
			return strChNum[i/100] + strChDig[2] + strChNum[1] + ChineseNumber (i%100);
		else return strChNum[i/100] + strChDig[2] +	ChineseNumber (i%100);
	}
	if( i<10000 ) {
		if( i%1000==0 )
			return strChNum[i/1000] + strChDig[3];
		else if( i%1000	< 100 )
			return strChNum[i/1000] + strChDig[3] + strChDig[0] + ChineseNumber (i%1000);
		else
			return strChNum[i/1000] + strChDig[3] + ChineseNumber (i%1000);
	}
	if( i<100000000	) {
		if( i%10000==0 )
			return ChineseNumber (i/10000) + strChDig[4];
		else if( i%10000 < 1000	)
			return ChineseNumber (i/10000) + strChDig[4] + strChDig[0] + ChineseNumber (i%10000);
		else
			return ChineseNumber (i/10000) + strChDig[4] + ChineseNumber (i%10000);
	}
	if( i<1000000000000 ) {
		if( i%100000000==0 )
			return ChineseNumber (i/100000000) + strChDig[5];
		else if( i%100000000 < 10000000	)
			return ChineseNumber (i/100000000) + strChDig[5]	+ strChDig[0] + ChineseNumber (i%100000000);
		else
			return ChineseNumber (i/100000000) + strChDig[5]	+ ChineseNumber (i%100000000);
	}
		if( i%1000000000000==0 )
			return ChineseNumber (i/1000000000000) + strChDig[6];
		else if( i%1000000000000 < 100000000000	)
			return ChineseNumber (i/1000000000000) + strChDig[6] + strChDig[0] + ChineseNumber (i%1000000000000);
		else
			return ChineseNumber (i/1000000000000) + strChDig[6] + ChineseNumber (i%1000000000000);
}

bool IsChinese(const std::string &str)
{
	if( str.length () < 2 ) return false;

	int i;
	for( i= 0; i < str.length (); i++) {
		unsigned char asc = str[i];
		if( asc < 161 || asc == 255 )
			return false;
		if( !(i%2) && (asc < 176 || asc >= 248) )
			return false;
	}
	return true;
}

}
