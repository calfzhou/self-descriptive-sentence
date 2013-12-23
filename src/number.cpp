#include "number.h"

namespace Number {

static std::string strChDig[] =
    { "零","十","百","千","万","亿","兆" };
static std::string strChNum[] =
    {"零","一","二","三","四","五","六","七","八","九","十"};

std::string NumberNumber(int i)
{
    char buf[16];
    sprintf(buf, "%d", i);
    return buf;
}

bool IsNumber(const std::string &str)
{
    int i;
    for( i= 0; i < str.length (); i++)
    {
        if (str[i] < '0' || str[i] > '9')
            return false;
    }
    return true;
}

}
