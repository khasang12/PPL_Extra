# premable
main:
	li $s1, 1
	li $s0, 2
	sub $s1, $s1, $s0
	addi $a0, $s1 ,0
	li $v0, 1
	syscall
