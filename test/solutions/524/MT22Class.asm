# premable
main:
	li $s0, 5
	li $s0, 5
Label4:
	li $t0, 0
	sub $t0, $s0, $t0
	slt $t1, $zero, $t0
	beq $t1, $zero, Label3
Label5:
	li $t0, 3
	sub $t0, $s0, $t0
	slt $t1, $zero, $t0
	beq $t1, $zero, Label9
	j Label2
Label9:
	addi $a0, $s0 ,0
	li $v0, 1
	syscall
Label2:
Label6:
	subi $s0, $s0, 1
	j Label4
Label3:
