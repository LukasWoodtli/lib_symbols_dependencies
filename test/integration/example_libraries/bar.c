#include <stdio.h>

void bar(void) {
	printf("In function %s", __PRETTY_FUNCTION__);
}
