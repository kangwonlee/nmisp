import pytest

from . import get_cpp_from_ipynb as gcpp

cpp_compile_test_case = """// Begin account_module_user.cpp
#include <iostream>
#include <cstdint>

namespace account_a{
    #include "account_module.h"
}

namespace account_b{
    #include "account_module.h"
}

using namespace std;

int32_t main(int32_t argn, char ** argv){

}
"""

cpp_test_cases = [
    ("""
void main (){
}
""", True),

    ("""
int main (int argn, char * argv[]){
    return 0;
}
""", True),

    ("""
int mann (int argn, char * argv[]){
    return 0;
}
""", False),

    ("""
int mann (int argn, char * argv[]){
    return main(a, b);
}
""", False),

    ("""#include <iostream>
#include <cstdint>

namespace account_a{
    #include "account_module.h"
}

namespace account_b{
    #include "account_module.h"
}

using namespace std;

int32_t main (int argn, char * argv[]){
    return 0;
}
""", True),
    (cpp_compile_test_case, True),
    ('''// ``` C++
// Begin account_module.h
#include <cstdint>


void deposit (int32_t amount);
void withdraw (int32_t amount);
int32_t check();
// End account_module.h\n// ```''', False)
]


# https://docs.pytest.org/en/latest/example/parametrize.html
@pytest.mark.parametrize("cpp_txt, expected", cpp_test_cases)
def test_get_main_function_pattern1(cpp_txt, expected):
    r = gcpp.get_main_function_pattern()

    result = r.findall(cpp_txt)
    message = f"Unable to match case :{cpp_txt}"

    if expected:
        assert result, message
    else:
        assert not (result), message
