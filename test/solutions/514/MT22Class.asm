# premable
main:
	li $s0, 1
	li $t0, 0
	sub $t0, $s0, $t0
	slt $t1, $zero, $t0
	beq $t1, $zero, Label3
	li $t0, 5
	sub $t0, $s0, $t0
	addi $t1, $t0, 0
	beq $t1, $zero, Label5
	li $t0, 6
	addi $a0, $t0, 0
	li $v0, 1
	syscall
Label5:
Label3:
