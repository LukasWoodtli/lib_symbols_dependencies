#include <stdio.h>

#include "baz.h"
#include "foo.h"

void baz(void) {
	printf("In function %s", __PRETTY_FUNCTION__);
	printf("Calling foo");
	foo();
}
