section .text
    global _start

    _start:
        mov rcx, counter
        
    loop_start:
        mov rax, 1
        mov rdi, 1
        mov rsi, base_filename
        mov rdx, extension
        mov r10, rcx
        call construct_filename

        mov rax, 2
        lea rdi, [rel filename]
        mov rsi, 0x0211
        mov rdx, 0644
        syscall

        cmp rax, 0
        jl error

        mov rdi, rax
        mov rax, 1
        mov rsi, buffer
        mov rdx, bufferLen
        syscall

        mov rax, 3
        syscall

        dec rcx
        cmp rcx, 0
        jnz loop_start

        mov rax, 60
        mov rdi, 42
        syscall

    construct_filename:
        push rbx
        push r11

        mov rbx, 10
        xor r11, r11

        filename_loop:
            xor rdx, rdx
            div rbx
            add dl, '0'
            dec rsi
            mov byte [rsi], dl
            inc r11
            test rax, rax
            jnz filename_loop

        mov byte [rsi], '+'

        pop r11
        pop rbx
        ret

    error:
        mov rax, 1
        mov rdi, 1
        mov rsi, errorm
        mov rdx, errormLen
        syscall 

        mov rax, 60
        mov rdi, 0
        syscall
        

section .data
    base_filename: db "quine", 0
    filenameLen: equ $-base_filename
    extension: db ".txt", 0

    buffer: db "this is a test", 0
    bufferLen: equ $-buffer

    errorm: db "An error occurred.", 0
    errormLen: equ $-errorm

    counter: equ 5

section .bss
    filename resb 16
