%macro pushd 0
    push rax
    push rbx
    push rcx
    push rdx
%endmacro
%macro popd 0
    pop rdx
    pop rcx
    pop rbx
    pop rax
%endmacro
%macro print 2
    pushd
    mov rax, 1
    mov rdi, 1
    mov rsi, %1
    mov rdx, %2
    syscall
    popd
%endmacro
%macro dprint 0
    pushd
    mov rcx, 10
    mov rbx, 0
    %%divide:
        xor rdx, rdx
        div rcx
        push rdx
        inc rbx
        cmp rax, 0
        jne %%divide
    %%digit:
        pop rax
        add rax, '0'
        mov [result], rax
        print result,1
        dec rbx
        cmp rbx, 0
        jg %%digit
    popd
%endmacro
%macro arrsum 2
  mov rdx,0
  mov al,0
  %%cycle:
      add al, [%1 + rdx]
      inc rdx
      cmp rdx, %2
      jl %%cycle
      
%endmacro
%macro subprint 3
    pushd
    mov rdx, %1
    mov rbx, %2
    print dotsymb, 1
    mov rcx, 0
    %%drob:
        inc rcx
        mov rax, 10
        mul rdx
        div rbx
        dprint
        mov rax, 0
        cmp rcx, %3
        jg %%end
        cmp rdx, rax
        jg %%drob
    %%end:
        popd
%endmacro
section .text
global _start

_start:
    arrsum y, ylen
    mov bl, al
    arrsum x, xlen
    sub al, bl
    mov cl, 128
    cmp al, cl
    jl printans
    mov cl, al
    mov al, 256
    sub al, cl
    xor dl, dl
    mov rbx, reallen
    div rbx
printans:
    dprint
    subprint rdx, rbx, 2
    print newline, nlen
    print done, len
    mov rax, 60
    xor rdi, rdi
    syscall

section .data
    x dd 5, 3, 2, 6, 1, 7, 4
    y dd 0, 10, 1, 9, 2, 8, 5
    xlen equ ($-x)/2
    ylen equ $-y
    reallen equ ($-x)/8
    dotsymb db ".",0xA, 0xD
    done db "Done",0xA, 0xD
    len equ $ - done
    newline db 0xA, 0xD
    nlen equ $ - newline

section .bss
    result resb 1
    
    
