# premable
main:
	li $s1, 3
	li $s0, 2
	mult $s1, $s0
	mflo $s1
	addi $a0, $s1 ,0
	li $v0, 1
	syscall
