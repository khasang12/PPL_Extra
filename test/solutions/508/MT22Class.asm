# premable
main:
	li $s1, 1
	li $s0, 2
	add $s1, $s1, $s0
	li $s1, 1
	addi $s0, $s1, 1
	addi $s1, $zero, 1
	addi $s1, $s1, 2
	addi $a0, $s1 ,0
	li $v0, 1
	syscall
	addi $a0, $s0 ,0
	li $v0, 1
	syscall
