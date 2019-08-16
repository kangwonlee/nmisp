# https://stackoverflow.com/questions/35160256/how-do-i-output-lists-as-a-table-in-jupyter-notebook
# http://nbviewer.jupyter.org/github/ipython/ipython/blob/4.0.x/examples/IPython%20Kernel/Rich%20Output.ipynb

# import modules to extend python's features
import math      # math functions and constants
import IPython   # ipython notebook features

# MarkDown is like a simplified version of html
# Using MarkDown, for example, we can present a table


def get_binary_hex_decimal_table():

    # Following lines designate the header of a markdown table
    rows_list = ['''| Decimal | Binary | no. bits | no. bytes | Hexadecimal |
    |:--------------:|:------------:|:------------:|:------------:|:-------------------:|''']
    # To add the table body, following for loop will add more lines
    # to this list. 

    # Decimal number loop == Table body loop
    for i in list(range(0, 21)) + [127, 128, 255, 256, 32767, 32768, 65535, 65536, 2**32-1, 2**32, 2**63-1, 2**63, 2**64-1, 2**64, ]:

        # First column : Decimal format
        d_str = str(i)

        # Second column : Binary format
        b_str = f"{i:b}"

        # Third column : Number of bits
        n_bits = len(b_str)
        n_bits_str = str(len(b_str))
        
        # if binary format is too long, do not indicate
        # otherwise, the second column would take too much space
        if 17 < n_bits:
            b_str = '...'

        # Fifth column : Hexadecimal format
        h_str = f"{i:X}"

        # Fourth column : Number of bytes
        # Try `help(math.ceil)` to check what it does
        n_bytes = math.ceil(len(h_str) * 0.5)
        n_bytes_str = str(n_bytes)

        # Indicate a row of the table
        # using variables above
        rows_list.append('|'.join(['', d_str, b_str, n_bits_str, n_bytes_str, h_str, '']))

    return rows_list


def unsigned_sigined_int(n):
        
    # start the list for rows of table with header rows
    table = [ f''' {n} bit bit pattern | `unsigned int{n}_t` | `signed int{n}_t` 
    :-----------------:|:--------:|:------:''']

    # table body : 0 ~ 3
    for i in range(0, 3):
        table.append(f'{i:0{n}b} | {i} | {i}')

    # to make the table shorter add ellipsis
    table.append(f' ... | ... | ... ')

    # rows around the change of the sign
    # positive
    for i in range(2**(n-1)-2, 2**(n-1)-1+1):
        table.append(f'{i:0{n}b} | {i} | {i}')

    # negative
    for i in range(2**(n-1), 2**(n-1)+2+1):
        table.append(f'{i:0{n}b} | {i} | {i-(2**n)}')

    # to make the table shorter add ellipsis
    table.append(f' ... | ... | ... ')

    # rows close to the n bit limit
    for i in range((2**n)-2, (2**n)-1+1):
        table.append(f'{i:0{n}b} | {i} | {i-(2**n)}')

    return table


def get_float_bits(n, ne):
    ns = n - 1 - ne # number of significand bits
    return [
        # header row : position of bits
        ' | '.join(str(k) for k in range(n-1, 0 - 1, -1)), 
        # separator row
        '|'.join(':---:' for k in range(1, n+1)),
        # body row
        ' | '.join([r'$\pm$'] + ['`e`']*ne + ['`s`']*ns),
    ]


def present_table(table):
    IPython.display.display(
        IPython.display.Markdown(
            '\n'.join(table) # Connect all elements of the list
        )    # Create a Markdown table (let's put it this way for now)
    )    # Indicate as a Markdown table
