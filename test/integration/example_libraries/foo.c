#include <stdio.h>

#include "bar.h"

void foo(void) {
	printf("In function %s", __PRETTY_FUNCTION__);
	printf("Calling bar");
	bar();
}
