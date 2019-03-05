package edu.colorado.csci3155.project1


sealed trait StackMachineInstruction
case object AddI extends StackMachineInstruction
case object SubI extends StackMachineInstruction
case object MultI extends StackMachineInstruction
case object DivI extends StackMachineInstruction
case object ExpI extends StackMachineInstruction
case object LogI extends StackMachineInstruction
case object SinI extends StackMachineInstruction
case object CosI extends StackMachineInstruction
case class PushI(f: Double) extends StackMachineInstruction
case object PopI extends StackMachineInstruction


object StackMachineEmulator {

    def computeResultsBinary(stack: List[Double], f: (Double, Double) => Double, isDiv: Boolean): List[Double] = {
      if(stack.length < 2) {
        throw new IllegalArgumentException("Stack length is less than 2")
      }
      else {
        if(isDiv && stack(1) == 0)
          throw new IllegalArgumentException("Cannot divide by zero")
        else {
          val res = f(stack(1), stack(0))
          res :: stack.slice(2, stack.length)
        }
      }
    }

    def computResultUnary(stack: List[Double], f: (Double) => Double, isLog: Boolean): List[Double] = {
      if(stack.isEmpty)
        throw new IllegalArgumentException("Stack is empty")
      else {
        if(isLog && stack(0) < 0)
          throw new IllegalArgumentException("Cannot take log of a negative number")
        else {
          val res = f(stack(0))
          res :: stack.slice(1, stack.length)
        }
      }
    }

    /* Function emulateSingleInstruction
        Given a list of doubles to represent a stack and a single instruction of type StackMachineInstruction
        Return a stack that results when the instruction is executed from the stack.
        Make sure you handle the error cases: eg., stack size must be appropriate for the instruction
        being executed. Division by zero, log of a non negative number
        Throw an exception or assertion violation when error happens.

     */
    def emulateSingleInstruction(stack: List[Double], ins: StackMachineInstruction): List[Double] = {
        ins match {
          case PushI(f) => {
            f :: stack
          }
          case PopI => {
            if (stack.isEmpty)
              throw new IllegalArgumentException("Stack is empty")
            else
              stack.slice(1, stack.length)
          }
          case AddI => {
            computeResultsBinary(stack, (x, y) => x + y, false)
          }
          case SubI => {
            computeResultsBinary(stack, (x, y) => x - y, false)
          }
          case MultI => {
            computeResultsBinary(stack, (x, y) => x * y, false)
          }
          case DivI => {
            computeResultsBinary(stack, (x, y) => x / y, true)
          }
          case LogI => {
            computResultUnary(stack, x => math.log(x), true)
          }
          case ExpI => {
            computResultUnary(stack, x => math.exp(x), false)
          }
          case SinI => {
            computResultUnary(stack, x => math.sin(x), false)
          }
          case CosI => {
            computResultUnary(stack, x => math.cos(x), false)
          }
        }
    }

    /* Function emulateStackMachine
       Execute the list of instructions provided as inputs using the
       emulateSingleInstruction function.
       Use foldLeft over list of instruction rather than a for loop if you can.
       Return value must be a double that is the top of the stack after all instructions
       are executed.
     */
    def emulateStackMachine(instructionList: List[StackMachineInstruction]): Double = {
      val stack = instructionList.foldLeft(List[Double]())(emulateSingleInstruction)

      stack(0)
    }
}