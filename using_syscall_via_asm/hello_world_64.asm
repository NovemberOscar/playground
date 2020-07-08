        section    .text
        global     _main
_main:
        mov        rax, 4
        add        rax, 0x2000000 ;MacOS & BSD
        mov        rdi, 1
        mov        rsi, msg
        mov        rdx, len
        syscall 

        mov        rax, 1
        add        rax, 0x2000000 ;MacOS & BSD
        mov        rdi, 0
        syscall 

        section    .data
msg:    db         'Hello, world!', 10
len:    equ   	   $ - msg	
