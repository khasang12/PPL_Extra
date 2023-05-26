# preamble
main:
	li $s1, 1
	li $s0, 2
	li $s0, 3
	addi $s0, $s0, 0
	add $s1, $s1, $s0
	addi $a0, $s1 ,0
	li $v0, 1
	syscall
