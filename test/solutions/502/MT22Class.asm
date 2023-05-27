# premable
main:
	li $s0, 1
	li $s1, 2
	li $s2, 3
	add $s1, $s0, $s1
	add $s3, $s1, $s0
	add $s0, $s0, $s1
	addi $s1, $s3, 1
	addi $s1, $s2, 0
	add $s0, $s0, $s1
	addi $a0, $s0 ,0
	li $v0, 1
	syscall
