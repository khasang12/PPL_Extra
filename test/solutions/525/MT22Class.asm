# premable
main:
	li $s0, 10
Label2:
	li $t0, 15
	sub $t0, $s0, $t0
	slt $t1, $t0, $zero
	beq $t1, $zero, Label3
	li $t0, 3
	sub $t0, $s0, $t0
	slt $t1, $zero, $t0
	beq $t1, $zero, Label6
	addi $s0, $s0, 1
	j Label2
Label6:
	addi $a0, $s0 ,0
	li $v0, 1
	syscall
	addi $s0, $s0, 1
	j Label2
Label3:
