# premable
main:
	li $s0, 1
	li $t0, 1
	sub $t0, $s0, $t0
	slt $t1, $zero, $t0
	beq $t1, $zero, Label3
	li $t0, 1
	addi $a0, $t0, 0
	li $v0, 1
	syscall
	j Label4
Label3:
	li $t0, 0
	addi $a0, $t0, 0
	li $v0, 1
	syscall
Label4:
	li $t0, 1
	sub $t0, $s0, $t0
	slt $t1, $t0, $zero
	beq $t1, $zero, Label6
	li $t0, 0
	addi $a0, $t0, 0
	li $v0, 1
	syscall
	j Label7
Label6:
	li $t0, 1
	addi $a0, $t0, 0
	li $v0, 1
	syscall
Label7:
	li $t0, 1
	sub $t0, $s0, $t0
	slt $t1, $zero, $t0
	bne $t1, $zero, Label9
	li $t0, 1
	addi $a0, $t0, 0
	li $v0, 1
	syscall
	j Label10
Label9:
	li $t0, 0
	addi $a0, $t0, 0
	li $v0, 1
	syscall
Label10:
	li $t0, 1
	sub $t0, $s0, $t0
	slt $t1, $zero, $t0
	bne $t1, $zero, Label12
	li $t0, 1
	addi $a0, $t0, 0
	li $v0, 1
	syscall
	j Label13
Label12:
	li $t0, 0
	addi $a0, $t0, 0
	li $v0, 1
	syscall
Label13:
