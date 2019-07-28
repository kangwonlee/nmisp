import pytest

from . import get_cpp_from_ipynb as gcpp

cpp_compile_test_case = """//```\n// Begin account_module_user.cpp
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
    ('\n// ``` C++\n// Begin account_module_user.cpp\n#include <iostream>\n#include <cstdint>\n\n#include "account_module.h"\n\nusing namespace std;\n\nint32_t main(int32_t argn, char * argv[]){\n\n    cout << "account_module.check() = "<< check() <<\'\\n\';\n\n    deposit(10000);\n\n    cout << "account_module.check() = "<< check() <<\'\\n\';\n\n    withdraw(3000);\n\n    cout << "account_module.check() = "<< check() <<\'\\n\';\n\n    deposit(5000);\n\n    cout << "account_module.check() = "<< check() <<\'\\n\';\n\n    return 0;\n}\n// End account_module_user.cpp\n// Build command : g++ -Wall -g account_module.cpp account_module_user.cpp -o account_module_user\n// ```\n\n', 
    'g++ -Wall -g account_module.cpp account_module_user.cpp -o account_module_user'),
    ('\n// ``` C++\n// Begin account_module_user.cpp\n#include <iostream>\n#include <cstdint>\n\n#include "account_module.h"\n\nusing namespace std;\n\nint32_t main(int32_t argn, char ** argv){\n\n    cout << "account_module.check() = "<< account::check() <<\'\\n\';\n\n    account::deposit(10000);\n\n    cout << "account_module.check() = "<< account::check() <<\'\\n\';\n\n    account::withdraw(3000);\n\n    cout << "account_module.check() = "<< account::check() <<\'\\n\';\n\n    account::deposit(5000);\n\n    cout << "account_module.check() = "<< account::check() <<\'\\n\';\n\n    return 0;\n}\n// End account_module_user.cpp\n// Build command : g++ -Wall -g account_module.cpp account_module_user.cpp -o account_module_user\n// ```\n\n', 
    'g++ -Wall -g account_module.cpp account_module_user.cpp -o account_module_user'),
    ('// ``` C++\n// Begin account_module.h\n#include <cstdint>\n\nvoid deposit (int32_t amount);\nvoid withdraw (int32_t amount);\nint32_t check();\n// End account_module.h\n// ```', 
    ''),
    ('// ``` C++\n// Begin account_module.cpp\n#include <iostream>\n#include <cstdint>\n\n#include "account_module.h"\n\nusing namespace std;\n\nint32_t balance;\n\n\nvoid deposit (int32_t amount){\n    cout << "Deposit " << amount << \'\\n\';\n    balance += amount;\n}\n\n\nvoid withdraw (int32_t amount){\n    cout << "Depowithdrawsit " << amount << \'\\n\';\n    balance += -amount;\n}\n\n\nint32_t check(){\n    return balance;\n}\n// End account_module.cpp\n// ```\n\n', 
    ''),
    ('\n// ``` C++\n// Begin account_module_user.cpp\n#include <iostream>\n#include <cstdint>\n\n#include "account_module.h"\n\nusing namespace std;\n\nint32_t main(int32_t argn, char * argv[]){\n\n    cout << "account_module.check() = "<< check() <<\'\\n\';\n\n    deposit(10000);\n\n    cout << "account_module.check() = "<< check() <<\'\\n\';\n\n    withdraw(3000);\n\n    cout << "account_module.check() = "<< check() <<\'\\n\';\n\n    deposit(5000);\n\n    cout << "account_module.check() = "<< check() <<\'\\n\';\n\n    return 0;\n}\n// End account_module_user.cpp\n// ```\n\n', 
    ''),
    ('// ``` C++\n// Begin account_module.h\n#include <cstdint>\n\nnamespace account {\n    void deposit (int32_t amount);\n    void withdraw (int32_t amount);\n    int32_t check();\n}\n// End account_module.h\n// ```', 
    ''),
    ('// ``` C++\n// Begin account_module.cpp\n#include <iostream>\n#include <cstdint>\n\n#include "account_module.h"\n\nusing namespace std;\n\nnamespace account{\n    int32_t balance;\n\n    void deposit (int32_t amount){\n        cout << "Deposit " << amount << \'\\n\';\n        balance += amount;\n    }\n\n    void withdraw (int32_t amount){\n        cout << "Depowithdrawsit " << amount << \'\\n\';\n        balance += -amount;\n    }\n\n    int32_t check(){\n        return balance;\n    }\n}\n// End account_module.cpp\n// ```\n\n', 
    ''),
    ('\n// ``` C++\n// Begin account_module_user.cpp\n#include <iostream>\n#include <cstdint>\n\n#include "account_module.h"\n\nusing namespace std;\n\nint32_t main(int32_t argn, char ** argv){\n\n    cout << "account_module.check() = "<< account::check() <<\'\\n\';\n\n    account::deposit(10000);\n\n    cout << "account_module.check() = "<< account::check() <<\'\\n\';\n\n    account::withdraw(3000);\n\n    cout << "account_module.check() = "<< account::check() <<\'\\n\';\n\n    account::deposit(5000);\n\n    cout << "account_module.check() = "<< account::check() <<\'\\n\';\n\n    return 0;\n}\n// End account_module_user.cpp\n// ```\n\n', 
    ''),
    ('// ``` C++\n// Begin account_module.h\n#include <cstdint>\n#include <iostream>\n\nint32_t balance;\n\n\nvoid deposit (int32_t amount){\n    std::cout << "Deposit " << amount << \'\\n\';\n    balance += amount;\n}\n\n\nvoid withdraw (int32_t amount){\n    std::cout << "Depowithdrawsit " << amount << \'\\n\';\n    balance += -amount;\n}\n\n\nint32_t check(){\n    return balance;\n}\n// End account_module.h\n\n// ```', 
    ''),
    ('// ```C++\n// Begin account_module_user.cpp\n#include <iostream>\n#include <cstdint>\n\nnamespace account_a{\n    #include "account_module.h"\n}\n\nnamespace account_b{\n    #include "account_module.h"\n}\n\nusing namespace std;\n\nint32_t main(int32_t argn, char ** argv){\n\n    cout << "account_a::check() = "<< account_a::check() <<\'\\n\';\n    cout << "account_b::check() = "<< account_b::check() <<\'\\n\';\n\n    account_a::deposit(10000);\n\n    cout << "account_a::check() = "<< account_a::check() <<\'\\n\';\n    cout << "account_b::check() = "<< account_b::check() <<\'\\n\';\n\n    account_a::withdraw(3000);\n\n    cout << "account_a::check() = "<< account_a::check() <<\'\\n\';\n    cout << "account_b::check() = "<< account_b::check() <<\'\\n\';\n\n    account_a::deposit(5000);\n\n    cout << "account_a::check() = "<< account_a::check() <<\'\\n\';\n    cout << "account_b::check() = "<< account_b::check() <<\'\\n\';\n\n    remurn 0;\n}\n// End account_module_user.cpp\n// ```', 
    ''),
    ("""//```
void main (){
}
""", ""),

    ("""// ```
int main (int argn, char * argv[]){
    return 0;
}
""", ""),

    ("""// ```
int mann (int argn, char * argv[]){
    return 0;
}
""", ""),

    ("""// ```
int mann (int argn, char * argv[]){
    return main(a, b);
}
""", ""),

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
""", ""),
    (cpp_compile_test_case, ""),
    ('''// ``` C++
// Begin account_module.h
#include <cstdint>


void deposit (int32_t amount);
void withdraw (int32_t amount);
int32_t check();
// End account_module.h\n// ```''', "")
]


# https://docs.pytest.org/en/latest/example/parametrize.html
@pytest.mark.parametrize("cpp_txt, expected", cpp_test_cases)
def test_get_build_command_in_last_line(cpp_txt, expected):
    result = gcpp.get_build_command_in_last_line(cpp_txt)
    message = f"\nexpected : {expected}\nresult : {result}"

    assert result == expected, message
