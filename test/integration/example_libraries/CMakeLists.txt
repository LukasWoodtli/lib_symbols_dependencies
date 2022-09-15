cmake_minimum_required(VERSION 3.1)

project(FooBar)

set(CMAKE_LIBRARY_OUTPUT_DIRECTORY lib)

add_library(foo SHARED foo.h foo.c)
target_link_libraries(foo PRIVATE bar)

add_library(bar SHARED bar.h bar.c)

add_library(baz SHARED baz.h baz.c)
target_link_libraries(baz PRIVATE foo)
