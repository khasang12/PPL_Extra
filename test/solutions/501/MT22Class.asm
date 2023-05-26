# preamble
main:
	li $s0, 1
	li $s1, 2
	li $s2, 4
	add $s2, $s0, $s1
	addi $a0, $s2 ,0
	li $v0, 1
	syscall
