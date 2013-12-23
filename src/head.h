#include <time.h>
#include <stdlib.h> 
#include <string>

#define Randomize() srand (time(NULL))
#define RandomMax() rand()
#define Random(n) rand()%n

void test();
void GetString(std::string &);

// 初始分析，为特殊字建立初始计数
void init(int *, int *, int, const std::string &);
// 对特殊字的计数做一次变换，由前两次的数值确定新的数值
// 若前两次数值完全一样，则返回true
bool calc(int *, int *, int);
// 在特殊字计数数组中去掉某整数的文字串中相应的特殊字
void dosub(int *, int, int);
// 在特殊字计数数组中加入某整数的文字串中相应的特殊字
void doadd(int *, int, int);
// 给某个特殊字计数值加1
void doinc(int *, int, int);
// 判断数字在特殊字组中的位置
int ch2idx(char);
// 打印特殊字计数数组
void print(int *, int, bool newline = false);
// 打印最终结果（带标点）
void output(const std::string &, int *, int);
// 打印最终结果（不带标点）
void output2(const std::string &, int *, int);
// 复制数组
void copy(int *, int *, int);
