# premable
main:
	li $s1, 6
	li $s0, 2
	div $s1, $s0
	mfhi $s1
	addi $a0, $s1 ,0
	li $v0, 1
	syscall
