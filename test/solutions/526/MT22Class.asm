# premable
main:
	li $s0, 5
	li $s0, 2
Label4:
	li $t0, 0
	sub $t0, $s0, $t0
	slt $t1, $zero, $t0
	beq $t1, $zero, Label3
Label5:
	li $s1, 0
	li $s1, 2
Label10:
	li $t0, 0
	sub $t0, $s1, $t0
	slt $t1, $zero, $t0
	beq $t1, $zero, Label9
Label11:
	sub $t0, $s0, $s1
	addi $t1, $t0, 0
	bne $t1, $zero, Label15
	j Label8
	j Label16
Label15:
	addi $a0, $s1 ,0
	li $v0, 1
	syscall
	addi $a0, $s0 ,0
	li $v0, 1
	syscall
Label16:
Label8:
Label12:
	subi $s1, $s1, 1
	j Label10
Label9:
Label2:
Label6:
	subi $s0, $s0, 1
	j Label4
Label3:
