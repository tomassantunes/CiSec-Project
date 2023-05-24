section .data
    key db 0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c ; Example encryption key (128-bit)
    iv db 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f ; Example initialization vector (IV)
    input_file db "test.txt", 0
    output_file db "output.txt", 0

section .bss
    aes_key_expansion resb 240 ; AES key expansion buffer

section .text
    global _start

_start:
    ; Open the input file for reading
    mov rdi, input_file
    mov rsi, O_RDONLY
    xor rdx, rdx
    syscall
    mov r8, rax ; Store the file descriptor in r8

    ; Open the output file for writing
    mov rdi, output_file
    mov rsi, O_WRONLY | O_CREAT | O_TRUNC
    mov rdx, 0644 ; Permissions for the output file
    syscall
    mov r9, rax ; Store the file descriptor in r9

    ; Perform AES encryption
    mov rdi, r8 ; Input file descriptor
    mov rsi, r9 ; Output file descriptor
    mov rdx, AES_BLOCK_SIZE ; Buffer size (AES block size)
    lea rcx, [key] ; Encryption key
    lea rbp, [iv] ; Initialization vector
    call aes_encrypt_file

    ; Close the files
    mov rdi, r8 ; Input file descriptor
    mov rax, SYS_close
    syscall

    mov rdi, r9 ; Output file descriptor
    syscall

    ; Exit the program
    mov eax, SYS_exit
    xor edi, edi
    syscall

aes_encrypt_file:
    ; Allocate memory for the input and output buffers
    sub rsp, AES_BLOCK_SIZE
    mov r8, rsp ; Input buffer
    sub rsp, AES_BLOCK_SIZE
    mov r9, rsp ; Output buffer

    mov r11, 0 ; Total bytes read

read_loop:
    ; Read a block of data from the input file
    mov rax, SYS_read
    mov rdi, r8 ; Input file descriptor
    mov rsi, r8 ; Input buffer address
    mov rdx, AES_BLOCK_SIZE ; Read size (AES block size)
    syscall
    test rax, rax
    jz done

    ; Store the number of bytes read
    add r11, rax

    ; Perform AES encryption on the input buffer and store the result in the output buffer
    lea rdi, [aes_key_expansion]
    mov rsi, r8 ; Input buffer
    mov rdx, r9 ; Output buffer
    call aes_encrypt_block

    ; Write the encrypted block to the output file
    mov rax, SYS_write
    mov rdi, r9 ; Output file descriptor
    mov rsi, r9 ; Output buffer
    mov rdx, AES_BLOCK_SIZE ; Write size (AES block size)
    syscall

    jmp read_loop

done:
    add rsp, AES_BLOCK_SIZE
    add rsp, AES_BLOCK_SIZE
    ret

aes_encrypt_block:
    ; Perform AES encryption on a single block
    ; Input buffer (rsi) -> Output buffer (rdx)
    ; Key schedule (rdi) and IV (rbp) are already loaded

    ; AES key expansion
    call aes_key_expansion

    ; AES initial round
    movups xmm0, [rsi]
    movups xmm1, [rdi]
    addps xmm0, xmm1
    xorps xmm0, [rbp]
    movups [rdx], xmm0

    ; AES rounds
    mov ecx, AES_ROUNDS
    dec ecx
    movups xmm2, [rdi]
    movups xmm3, [rbp]
    .aes_rounds:
        aesenc xmm0, xmm2
        aesenclast xmm0, xmm3
        movups [rdx], xmm0
        add rdi, 16
        add rbp, 16
        add rdx, 16
        dec ecx
        jnz .aes_rounds

    ; AES final round
    aesenc xmm0, xmm2
    movups [rdx], xmm0

    ret

aes_key_expansion:
    ; Perform AES key expansion
    ; Key (rcx) -> Key schedule (rdi)

    ; Key setup
    movdqu xmm0, [rcx]
    movdqu xmm1, xmm0
    movdqu xmm2, xmm0
    movdqu xmm3, xmm0

    ; Key expansion rounds
    mov ecx, AES_EXPANSION_ROUNDS
    .key_expansion_rounds:
        movdqu xmm4, xmm3
        pslldq xmm4, 4
        movdqu xmm5, xmm3
        psrldq xmm5, 12
        movdqu xmm6, xmm2
        pslldq xmm6, 4
        xorps xmm6, xmm4
        xorps xmm6, xmm5
        movdqu xmm7, xmm1
        psrldq xmm7, 12
        xorps xmm6, xmm7
        movdqu xmm7, [rcx]
        add rcx, 16
        xorps xmm7, xmm6
        movdqu [rdi], xmm7
        add rdi, 16
        dec ecx
        jnz .key_expansion_rounds

    ret

section .text
    AES_BLOCK_SIZE equ 16
    SYS_read equ 0
    SYS_write equ 1
    SYS_close equ 3
    SYS_exit equ 60
    O_RDONLY equ 0
    O_WRONLY equ 1
    O_CREAT equ 64
    O_TRUNC equ 512
    AES_ROUNDS equ 10
    AES_EXPANSION_ROUNDS equ 14

