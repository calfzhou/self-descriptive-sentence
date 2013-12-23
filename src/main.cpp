#include <iostream>
#include <string>
#include <conio.h>

#include "number.h"
#include "head.h"

using namespace std;
// 防止死循环用的限制
// LIMIT1限制每次测试的递推深度
// LIMIT2限制测试的次数
#define LIMIT1 300
#define LIMIT2 50

const char CHS[] = "0123456789";
const int TOTAL = 10;

int main ()
{
    Randomize ();
    test ();
    return 0;
}

void test()
{
    string orgstr;  // 记录原始字串
    const int n = TOTAL;
    int *a1 = new int[n], *a2 = new int[n];  // a1,a2是特殊字计数数组,记录前后两次的结果
    int bk1[n], bk2[n];  // 备份用的数组
    int t1, t2 = 0;  // 记录calc执行次数，重复测试次数

    GetString (orgstr);  // 读取原始字串
    init (bk1, bk2, n, orgstr);  // 初始分析，结果保留在备份数组中

    cout << "开始计算，中途按'q'退出，其他键暂停或继续……" << endl;
    //print (bk2, n, true);
    while (t2++ < LIMIT2) {
        t1 = 0;
        bool succ = false;
        copy (bk1, a1, n);
        copy (bk2, a2, n);
        print (a1, n);
        print (a2, n);
        while ( !(succ = calc (a1, a2, n)) && t1 < LIMIT1) {
            // a1是较靠前的一次结果，a2是较靠后的
            t1 ++;
            /*cout << '(' << t2 << '-' << t1 << ')';/**/
            print (a1, n);
            if (kbhit ()) {
                if (getch () == 'q') exit (2);
                if (getch () == 'q') exit (2);
            }
            swap (a1, a2);  // calc将新的计数保存在a1中
        }
        if (!succ) continue;
        cout << endl;
        output (orgstr, a1, n);
        return;
    }
    cout << "\n我无能为力，或者运气太差：（" << endl;
}

bool calc(int *a1, int *a2, int n)
{
    // a1: old, a2: new
    int *temp = new int[n];
    int i;
    bool finish = true;

    for (i = 0; i < n; i++) {
        temp[i] = a1[i];
        a1[i] = a2[i];
    }
    // temp: old, a2: new, a1: dest(newest)
    for (i = 0; i < n; i++) {
        if (a2[i] == temp[i]) // nochange
            continue;
        finish = false;
        dosub (a1, n, temp[i]);
        doadd (a1, n, a2[i]);
    }
    // now a1 is the newest

    delete []temp;
    return finish;
}

void print(int *a, int n, bool newline)
{
    int i;
    /*for (i = 0; i < n; i++) {
        cout << CHS[i*2] << CHS[i*2+1] << "  ";
    }
    if (newline)
        cout << endl;
    else cout << '\r' << flush;/**/
    for (i = 0; i < n; i++) {
        cout.width (3);
        cout << a[i] << " ";
    }
    if (newline)
        cout << endl;
    else cout << '\r' << flush;
}

void dosub(int *a, int n, int num)
{
    string str = Number::NumberNumber (num);
    int i;
    int idx;

    if (num == 0)
        return;

    for (i = 0; i < str.length (); i++) {
        // 依次处理num的文字串中每个字
        idx = ch2idx (str[i]);
        if (a[idx] <= 1) {
            // 正常情况下不会执行这里
            cout << "Something wrong!!\nThe " << i << "th number too low:";
            print (a, n);
            exit (-1);
        }
        else if (a[idx] == 2 && Random (2)) {
            // 对于值为2的计数，可以将其变为0，也可以将其变为1
            // 若执行这段则变为0，否则变为1
            a[idx] --;
        }
        a[idx] --;
    }
}

void doinc(int *a, int n, int idx)
{
    // 把doinc放到doadd外面，因为有些地方需要直接调用doinc
    if (a[idx] < 0) {
        // 正常情况下不会执行这里
        cout << "Something wrong!!\nThe " << idx << "th number less than zero:";
        print (a, n);
        exit (-2);
    }
    if (a[idx] == 0) {
        // 对于值为0的计数，应使其变为2而非1
        a[idx] ++;
    }
    a[idx] ++;
}

void doadd(int *a, int n, int num)
{
    string str = Number::NumberNumber (num);
    int i;
    int idx;

    if (num == 0)
        return;

    for (i = 0; i < str.length (); i++) {
        // 依次处理num的文字串中每个字
        idx = ch2idx (str[i]);
        doinc (a, n, idx);
    }
}

inline int ch2idx(char c)
{
    return c-'0';
}

void init(int *a, int *b, int n, const string &s)
{
    int i, idx;

    for (i = 0; i < n; i++)
        a[i] = b[i] = 0;

    string str = s;

    for (i = 0; i < str.length (); i++) {
        idx = ch2idx (str[i]);
        doinc (b, n, idx);
    }
}

void GetString(string &str)
{
    cout << "输入数字串。\n"
        "输入英文字串\"empty\"作为空数字串。" << endl;
    cin >> str;
    if (str == "empty")
        str = "";
    else if (!Number::IsNumber (str)) {
        cout << "这个字符串不是数字串！" << endl;
        exit (1);
    }
}

void output(const std::string &str, int *a, int n)
{
    cout << str << "有";
    for (int i = 0; i < n; i++) {
        if (a[i] == 0) continue;
        cout << Number::NumberNumber (a[i])
            << "个" << CHS[i] << "，";
    }
    char bk = 8;
    cout << bk << bk << "。" << endl;
}

void copy(int *scr, int *dst, int n)
{
    for (int i = 0; i < n; i++)
        dst[i] = scr[i];
}
