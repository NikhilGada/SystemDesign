import queue
import time

class Lift(object):
	def __init__(self):
		self.currentFloor = 0
		self.upwardDestinationFloors = queue.Queue()
		self.downwardDestinationFloors = queue.Queue()
		self.direction = 0 
		self.express = False 

class Floor(object):
	def __init__(self, floorNumber):
		self.upward = False
		self.downward = False
		self.level = floorNumber
		self.riders = list()
		self.ridersGoingUp = list()
		self.ridersGoingDown = list()
	def setUp(self):
		if self.upward == True:
			print("Lift is already called to go up on floor ,d",self.level)
		else:
			self.upward = True
	def setDown(self):
		if self.downward == True:
			print("Lift is already called to go up on floor ,d", self.level)
		else:
			self.downward = True
	def getUpStatus(self):
		return self.upward
	def getDownStatus(self):
		return self.downward
	def clearDown(self):
		self.upward = False
	def clearUp(self):
		self.downward = False
	def getRiders(self):
		return self.riders
	def addPerson(self, person):
		self.riders.add(person)
		if person.destinationFloor > self.level:
			self.ridersGoingUp.add(person)
			setUp()
		elif person.destinationFloor < self.level:
			self.ridersGoingDown.add(person)
			setDown()
	def removePerson(self, direction):
		for person in self.riders:
			if person.destinationFloor > person.currentFloor and direction == 1:
				self.riders.remove(person)
				clearUp()
			elif person.destinationFloor < person.currentFloor and direction == -1:
				self.riders.remove(person)
				clearDown()
	def getRidersGoingUp(self, elevator):
		ridersEnteringLifts = self.ridersGoingUp
		self.ridersGoingUp = []
		self.clearUp()
		for person in ridersEnteringLifts:
			elevator.upwardDestinationFloors.put(person.destinationFloor)
			elevator.direction = 1
	def getRidersGoingDown(self, elevator):
		ridersEnteringLifts = self.ridersGoingDown
		self.ridersGoingDown = []
		self.clearDown()
		for person in ridersEnteringLifts:
			elevator.downwardDestinationFloors.put((-person.destinationFloor, person.destinationFloor))
			elevator.direction = -1		


class Person(object):
	def __init__(self, floor, destinationFloor):
		self.destinationFloor = destinationFloor
		self.currentFloor = floor
	def direction(self):
		if self.destinationFloor > self.currentFloor: 
			return 1 
		elif self.destinationFloor < self.currentFloor:
			return -1
		else:
		 	return 0



class LiftControlSystem(object):
	def __init__(self, total_elevators, total_floors, floorsNameSpace):
		self.requestOnFloor = set()
		self.managedLifts = [Lift() for x in range(total_elevators)]
		self.numberOfLifts = total_elevators
		self.maxfloors = total_floors
		self.floors = floorsNameSpace
	def update(self, elevator):

		if elevator.direction == 1 and self.floors[elevator.currentFloor].ridersGoingUp: self.floors[elevator.currentFloor].getRidersGoingUp(elevator)
		if elevator.direction == -1 and self.floors[elevator.currentFloor].ridersGoingDown: self.floors[elevator.currentFloor].getRidersGoingDown(elevator)
		if elevator.direction == 0 and self.floors[elevator.currentFloor].ridersGoingUp:
			self.floors[elevator.currentFloor].getRidersGoingUp(elevator)
		if elevator.direction == 0 and self.floors[elevator.currentFloor].ridersGoingDown:
			self.floors[elevator.currentFloor].getRidersGoingDown(elevator)		
	def step(self):
		for selectedLift in self.managedLifts:
			if selectedLift.upwardDestinationFloors.empty() and selectedLift.downwardDestinationFloors.empty():
				selectedLift.direction = 0 
				print(" Lift is remaining idle on floor " , (  selectedLift.currentFloor)) 
				self.update(selectedLift)
			else: 
				if (selectedLift.direction == 1 and not selectedLift.upwardDestinationFloors.empty()) or (selectedLift.direction == -1 and selectedLift.downwardDestinationFloors.empty() and not selectedLift.upwardDestinationFloors.empty()):
					selectedLift.direction == 1 					
					stopToRemember = selectedLift.upwardDestinationFloors.get()
					if selectedLift.currentFloor < stopToRemember:
						selectedLift.currentFloor = selectedLift.currentFloor + 1
						print(" Lift is moving past floor to destination" , (  selectedLift.currentFloor-1,
                                                                                                           selectedLift.currentFloor)) 
						selectedLift.upwardDestinationFloors.put(stopToRemember)
					if selectedLift.currentFloor == stopToRemember:
						print(" Lift is now open on floor " , (  selectedLift.currentFloor))
						if selectedLift.express == True: selectedLift.express = False 
						self.update(selectedLift)	
				elif (selectedLift.direction == -1 and not selectedLift.downwardDestinationFloors.empty()) or (selectedLift.direction == 1 and selectedLift.upwardDestinationFloors.empty() and not selectedLift.downwardDestinationFloors.empty()):
					selectedLift.direction == -1   
					stopToRemember = selectedLift.downwardDestinationFloors.get()[1]
					if selectedLift.currentFloor > stopToRemember:
						selectedLift.currentFloor = selectedLift.currentFloor - 1
						print(" s moving past floor ,d to floor ,d" ,
                                                      (  selectedLift.currentFloor+1,  selectedLift.currentFloor)) 
						selectedLift.downwardDestinationFloors.put((-stopToRemember,stopToRemember))
					if selectedLift.currentFloor == stopToRemember:
						print(" s says door is now open on floor ,d" , (  selectedLift.currentFloor))
						if selectedLift.express == True: selectedLift.express = False  
						self.update(selectedLift)
		

                        
	def pickup(self, floorNumber, direction):
		 
		for selectedLift in self.managedLifts:	
			
			if direction == selectedLift.direction and direction < 0 and selectedLift.express == False:
				for selectedLift in self.managedLifts:
					if selectedLift == self.managedLifts[0]:
					 	closestLift = selectedLift
					elif selectedLift.currentFloor - floorNumber < closestLift.currentFloor - floorNumber:
					 	closestLift = selectedLift
				closestLift.downwardDestinationFloors.put((-floorNumber,floorNumber))
				print("LCS sent elevator id:,s to floor ,d" , ( floorNumber))
				return
				""" Find closest elevators traveling upwards """
			elif direction == selectedLift.direction and direction > 0 and selectedLift.express == False:
				for selectedLift in self.managedLifts:
					if selectedLift == self.managedLifts[0]:
					 	closestLift = selectedLift
					elif floorNumber - selectedLift.currentFloor < floorNumber - closestLift.currentFloor:
					 	closestLift = selectedLift
				closestLift.upwardDestinationFloors.put(floorNumber)
				print("LCS sent elevator id:,s to floor ,d" , ( floorNumber))
				return
			else:
				""" Find closest unused elevator or default to the  first elevator """ 
				closestLift = self.managedLifts[0]
				for selectedLift in self.managedLifts:	
					if selectedLift.direction == 0:
						if selectedLift == self.managedLifts[0]:
						 	closestLift = selectedLift
						elif abs(selectedLift.currentFloor - floorNumber) < abs(closestLift.currentFloor - floorNumber):
						 	closestLift = selectedLift
				if closestLift.currentFloor > floorNumber:
					closestLift.direction = -1
					closestLift.downwardDestinationFloors.put((-floorNumber,floorNumber))
					closestLift.express = True
					print("LCS sent elevator id:,s to floor ,d" , (  floorNumber))
				elif closestLift.currentFloor < floorNumber:
					closestLift.direction = 1
					closestLift.upwardDestinationFloors.put(floorNumber)
					closestLift.express = True
					print("LCS sent elevator id:,s to floor ,d" , (  floorNumber))
				else:
					closestLift.direction = 0
					closestLift.express = False
					print("LCS opened elevator id:,s door for a person on floor ,d" , ( floorNumber))
					return


class Building(object):
	def __init__(self, TOTAL_FLOORS, TOTAL_LIFTS):
		self.floors = [Floor(i) for i in range(TOTAL_FLOORS)]
		self.lcs = LiftControlSystem(TOTAL_LIFTS, TOTAL_FLOORS, self.floors)
	def PersononFloor(self, person):
		self.floors[person.currentFloor].riders.append(person)
		print("user",self.floors)
		if person.direction() == 1: 
			self.floors[person.currentFloor].ridersGoingUp.append(person)
			self.floors[person.currentFloor].setUp()
			self.lcs.pickup(person.currentFloor, person.direction())
		if person.direction() == -1: 
			self.floors[person.currentFloor].ridersGoingDown.append(person)
			self.floors[person.currentFloor].setDown()
			self.lcs.pickup(person.currentFloor, person.direction())


	def run(self):
		while True:
		    self.lcs.step()
		    time.sleep(2)  
		    


def main():
	TOTAL_LIFTS = 3
	TOTAL_FLOORS = 8

	building = Building(TOTAL_FLOORS, TOTAL_LIFTS)
	Rahul = Person(0, 3)
	building.PersononFloor(Rahul)	
	building.run()

if __name__ == '__main__':
	main()
