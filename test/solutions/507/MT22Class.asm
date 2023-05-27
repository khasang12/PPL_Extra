# premable
main:
	li $s0, 1
	xori $s0, $s0, 1
	addi $a0, $s0 ,0
	li $v0, 1
	syscall
