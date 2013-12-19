#include <iostream>
#include <string>
#include <conio.h>

#include "chinese.h"
#include "head.h"

using namespace std;
// 防止死循环用的限制
// LIMIT1限制每次测试的递推深度
// LIMIT2限制测试的次数
#define LIMIT1 300
#define LIMIT2 50

const char CHS[] = "总个零一二三四五六七八九十百千万亿兆";  // "总"不是特殊字，在这里占位用
const int TOTAL = 36;  // CHS长度
const char GE[] = "个";

int main ()
{
	Randomize ();
	test ();
	return 0;
}

void test()
{
	string orgstr;  // 记录原始字串
	int n = TOTAL >> 1;
	int *a1 = new int[n];  // a1,a2是特殊字计数数组，第一个值为总字数
	int *a2 = new int[n];  // 用两个数组分别记录前后两次的结果
	int *bk1 = new int[n];  // 备份用的数组
	int *bk2 = new int[n];
	cf_list *cfl = new cf_list;  // 记录非特殊字字数的链表（头节点不记录数据）
	cfl->next = NULL;
	int t1, t2 = 0;  // 记录calc执行次数，重复测试次数

	GetString (orgstr);  // 读取原始字串
	init (bk1, bk2, n, orgstr, cfl);  // 初始分析，结果保留在备份数组中

	cout << "开始计算，中途按'q'退出，其他键暂停或继续……" << endl;
	print (bk2, n, true);
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
		output (orgstr, cfl, a1, n);
		cout << endl;
		output2 (orgstr, cfl, a1, n);
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
	string str = Chinese::ChineseNumber (num);
	int i;
	int idx;

	if (num == 0)
		return;

	for (i = 0; i < str.length (); i += 2) {
		// 依次处理num的文字串中每个字
		idx = cn2idx (str[i], str[i+1]);
		if (a[idx] <= 1) {
			// 正常情况下不会执行这里
			cout << "Something wrong!!\nThe " << i/2 << "th number too low:";
			print (a, n);
			exit (-1);
		}
		else if (a[idx] == 2 && Random (2)) {
			// 对于值为2的计数，可以将其变为0，也可以将其变为1
			// 若执行这段则变为0，否则变为1
			a[cn2idx (GE[0], GE[1])] --;
			a[idx] --;
			a[0] -= 2;  // "总"
		}
		a[idx] --;
		a[0] --;  // "总"
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
		a[cn2idx (GE[0], GE[1])] ++;
		a[idx] ++;
		a[0] += 2;  // "总"
	}
	a[idx] ++;
	a[0] ++;  // "总"
}

void doadd(int *a, int n, int num)
{
	string str = Chinese::ChineseNumber (num);
	int i;
	int idx;

	if (num == 0)
		return;

	for (i = 0; i < str.length (); i += 2) {
		// 依次处理num的文字串中每个字
		idx = cn2idx (str[i], str[i+1]);
		doinc (a, n, idx);
	}
}

int cn2idx(char c1, char c2)
{
	int idx;

	for (idx = 0; idx < TOTAL; idx += 2) {
		if (c1 == CHS[idx] && c2 == CHS[idx+1])
			return idx >> 1;
	}

	return -1;  // c1c2不在特殊字组中
	// 若c1c2=="总"，返回的是0，返回值大于0的才是真的特殊字
}

void init(int *a, int *b, int n, const string &s, cf_list *cflist)
{
	int i, idx;

	for (i = 0; i < n; i++)
		a[i] = b[i] = 0;

	string str = s + "这个句子一共有个字其中有";

	for (i = 0; i < str.length (); i += 2) {
		idx = cn2idx (str[i], str[i+1]);
		if (idx > 0) {  // 是特殊汉字
			doinc (b, n, idx);
		}
		else {  // 普通汉字
			bool exist = false;
			cf_list* pos = cflist;
			while (pos->next != NULL) {
				cf_list* curr = pos->next;
				if (str[i] == curr->val.a && str[i+1] == curr->val.b) {
					// 已经有了
					dosub (b, n, curr->val.fre);
					curr->val.fre ++;
					b[0] ++;  // "总"
					doadd (b, n, curr->val.fre);
					exist = true;
					break;
				}
				pos = pos->next;
			}
			if (exist) continue;
			// 新的汉字
			cf_list *cf = new cf_list;
			cf->val.a = str[i]; cf->val.b = str[i+1];
			cf->val.fre = 2; cf->next = NULL;
			b[0] += 2;  // "总"
			pos->next = cf;  // add to end of list
			doinc (b, n, cn2idx (GE[0], GE[1]));  // "个"增加一个
			doadd (b, n, 2);  // "二"增加一个
		}
	}
	/*cout << str << endl;
	cf_list* pos = cflist;
	while (pos->next != NULL) {
		cout << pos->next->val.fre << pos->next->val.a << pos->next->val.b;
		pos = pos->next;
	}
	cout << endl;/**/
}

void GetString(string &str)
{
	cout << "输入中文字符串，不带空格和标点。\n"
		"输入英文字串\"empty\"作为空中文字串。" << endl;
	cin >> str;
	if (str == "empty")
		str = "";
	else if (!Chinese::IsChinese (str)) {
		cout << "这个字符串不是中文字串！" << endl;
		exit (1);
	}
}

void output(const std::string &str, cf_list *cflist, int *a, int n)
{
	cout << str << "这个句子一共有"
		<< Chinese::ChineseNumber (a[0]) << "个字。其中有：";
	cf_list* pos = cflist->next;
	while (pos != NULL) {
		cout << Chinese::ChineseNumber (pos->val.fre)
			<< "个“" << pos->val.a << pos->val.b << "”；";
		pos = pos->next;
	}
	for (int i = 1; i < n; i++) {
		if (a[i] == 0) continue;
		cout << Chinese::ChineseNumber (a[i])
			<< "个“" << CHS[i*2] << CHS[i*2+1] << "”；";
	}
	char bk = 8;
	cout << bk << bk << "。" << endl;
}

void output2(const std::string &str, cf_list *cflist, int *a, int n)
{
	cout << str << "这个句子一共有"
		<< Chinese::ChineseNumber (a[0]) << "个字其中有";
	cf_list* pos = cflist->next;
	while (pos != NULL) {
		cout << Chinese::ChineseNumber (pos->val.fre)
			<< "个" << pos->val.a << pos->val.b;
		pos = pos->next;
	}
	for (int i = 1; i < n; i++) {
		if (a[i] == 0) continue;
		cout << Chinese::ChineseNumber (a[i])
			<< "个" << CHS[i*2] << CHS[i*2+1];
	}
	cout << endl;
}

void copy(int *scr, int *dst, int n)
{
	for (int i = 0; i < n; i++)
		dst[i] = scr[i];
}
