import os
import sys

import pytest

from . import get_cpp_from_ipynb as gcpp

cpp_test_cases = [
[{'cell_type': 'markdown', 'metadata': {}, 'source': '``` C++\n// Begin account_module.h\n#include <cstdint>\n\nvoid deposit (int32_t amount);\nvoid withdraw (int32_t amount);\nint32_t check();\n// End account_module.h\n```'},
{'result': 0, 'cpp_filename': 'account_module.h'}],
[{'cell_type': 'markdown', 'metadata': {}, 'source': '``` C++\n// Begin account_module.cpp\n#include <iostream>\n#include <cstdint>\n\n#include "account_module.h"\n\nusing namespace std;\n\nint32_t balance;\n\n\nvoid deposit (int32_t amount){\n    cout << "Deposit " << amount << \'\\n\';\n    balance += amount;\n}\n\n\nvoid withdraw (int32_t amount){\n    cout << "Depowithdrawsit " << amount << \'\\n\';\n    balance += -amount;\n}\n\n\nint32_t check(){\n    return balance;\n}\n// End account_module.cpp\n```\n\n'},
{'result': 0, 'cpp_filename': 'account_module.cpp'}],
[{'cell_type': 'markdown', 'metadata': {}, 'source': '\n``` C++\n// Begin account_module_user.cpp\n#include <iostream>\n#include <cstdint>\n\n#include "account_module.h"\n\nusing namespace std;\n\nint32_t main(int32_t argn, char * argv[]){\n\n    cout << "account_module.check() = "<< check() <<\'\\n\';\n\n    deposit(10000);\n\n    cout << "account_module.check() = "<< check() <<\'\\n\';\n\n    withdraw(3000);\n\n    cout << "account_module.check() = "<< check() <<\'\\n\';\n\n    deposit(5000);\n\n    cout << "account_module.check() = "<< check() <<\'\\n\';\n\n    return 0;\n}\n// End account_module_user.cpp\n// Build command : g++ -Wall -g account_module.cpp account_module_user.cpp -o account_module_user\n```\n\n'},
{'result': 0, 'cpp_filename': 'account_module_user.cpp'}],
[{'cell_type': 'markdown', 'metadata': {}, 'source': '``` C++\n// Begin account_module.h\n#include <cstdint>\n\nnamespace account {\n    void deposit (int32_t amount);\n    void withdraw (int32_t amount);\n    int32_t check();\n}\n// End account_module.h\n```'},
{'result': 0, 'cpp_filename': 'account_module.h'}],
[{'cell_type': 'markdown', 'metadata': {}, 'source': '``` C++\n// Begin account_module.cpp\n#include <iostream>\n#include <cstdint>\n\n#include "account_module.h"\n\nusing namespace std;\n\nnamespace account{\n    int32_t balance;\n\n    void deposit (int32_t amount){\n        cout << "Deposit " << amount << \'\\n\';\n        balance += amount;\n    }\n\n    void withdraw (int32_t amount){\n        cout << "Depowithdrawsit " << amount << \'\\n\';\n        balance += -amount;\n    }\n\n    int32_t check(){\n        return balance;\n    }\n}\n// End account_module.cpp\n```\n\n'},
{'result': 0, 'cpp_filename': 'account_module.cpp'}],
[{'cell_type': 'markdown', 'metadata': {}, 'source': '\n``` C++\n// Begin account_module_user.cpp\n#include <iostream>\n#include <cstdint>\n\n#include "account_module.h"\n\nusing namespace std;\n\nint32_t main(int32_t argn, char ** argv){\n\n    cout << "account_module.check() = "<< account::check() <<\'\\n\';\n\n    account::deposit(10000);\n\n    cout << "account_module.check() = "<< account::check() <<\'\\n\';\n\n    account::withdraw(3000);\n\n    cout << "account_module.check() = "<< account::check() <<\'\\n\';\n\n    account::deposit(5000);\n\n    cout << "account_module.check() = "<< account::check() <<\'\\n\';\n\n    return 0;\n}\n// End account_module_user.cpp\n// Build command : g++ -Wall -g account_module.cpp account_module_user.cpp -o account_module_user\n```\n\n'},
{'result': 0, 'cpp_filename': 'account_module_user.cpp'}],
[{'cell_type': 'markdown', 'metadata': {}, 'source': '``` C++\n// Begin account_module.h\n#include <cstdint>\n#include <iostream>\n\nint32_t balance;\n\n\nvoid deposit (int32_t amount){\n    std::cout << "Deposit " << amount << \'\\n\';\n    std::cout << "to " << & balance << \'\\n\';\n    balance += amount;\n}\n\n\nvoid withdraw (int32_t amount){\n    std::cout << "Withdraws " << amount << \'\\n\';\n    std::cout << "from " << & balance << \'\\n\';\n    balance += -amount;\n}\n\n\nint32_t check(){\n    return balance;\n}\n// End account_module.h\n\n```'},
{'result': 0, 'cpp_filename': 'account_module.h'}],
[{'cell_type': 'markdown', 'metadata': {}, 'source': '```C++\n// Begin account_module_user.cpp\n#include <iostream>\n#include <cstdint>\n\nnamespace account_a{\n    #include "account_module.h"\n}\n\nnamespace account_b{\n    #include "account_module.h"\n}\n\nusing namespace std;\n\nint32_t main(int32_t argn, char ** argv){\n\n    cout << "account_a::check() = "<< account_a::check() <<\'\\n\';\n    cout << "account_b::check() = "<< account_b::check() <<\'\\n\';\n\n    account_a::deposit(10000);\n\n    cout << "account_a::check() = "<< account_a::check() <<\'\\n\';\n    cout << "account_b::check() = "<< account_b::check() <<\'\\n\';\n\n    account_a::withdraw(3000);\n\n    cout << "account_a::check() = "<< account_a::check() <<\'\\n\';\n    cout << "account_b::check() = "<< account_b::check() <<\'\\n\';\n\n    account_b::deposit(5000);\n\n    cout << "account_a::check() = "<< account_a::check() <<\'\\n\';\n    cout << "account_b::check() = "<< account_b::check() <<\'\\n\';\n\n    return 0;\n}\n// End account_module_user.cpp\n```'},
{'result': 0, 'cpp_filename': 'account_module_user.cpp'}],
]


@pytest.mark.skipif(sys.platform.startswith("win"), reason="POSIX only for now")
def test_get_build_command_in_last_line():
    created_files = []
    for cpp_ipynb_md_cell, expected in cpp_test_cases:
        result = gcpp.build_markdown_cpp_cell(cpp_ipynb_md_cell)

        if os.path.exists(result["cpp_filename"]):
            created_files.append(result["cpp_filename"])

        # to delete during teardown
        if result['cpp_filename'] not in created_files:
            created_files.append(result['cpp_filename'])

        message = f"\nexpected : {expected}\nresult : {result}"

        assert result == expected, message

    for delete_this in created_files:
        if os.path.exists(delete_this):
            os.remove(delete_this)
