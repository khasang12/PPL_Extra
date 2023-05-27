# premable
main:
	li $s1, 1
	li $s0, 0
	and $s1, $s1, $s0
	or $s0, $s1, $s0
	andi $s1, $s1, 1
	ori $s0, $s0, 0
	addi $a0, $s1 ,0
	li $v0, 1
	syscall
	addi $a0, $s0 ,0
	li $v0, 1
	syscall
