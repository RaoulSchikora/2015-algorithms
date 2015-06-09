def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        pass
    return False


class IncidenceCell(object):
    def __init__(self, left, right, up, down, listHeader, name):
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.listHeader = listHeader
        self.name = name

    def representation(self):
        rep = ["c", self.name]
        for c in [self.left, self.right, self.up, self.down]:
            rep.append(c.name)
        return rep

    def rowRep(self):
        rep = "row " + self.name + ","
        curr = self.right
        while curr != self:
            rep += curr.name + ","
            curr = curr.right
        return rep

        
class ColumnObject(IncidenceCell):
    def __init__(self, left, right, up, down, name):
        IncidenceCell.__init__(self, left, right, up, down, self, name)
        self.size = 0

    def representation(self):
        hrep = ["h(" + str(self.size) + ")", self.name]
        for c in [self.left, self.right, self.up, self.down]:
            hrep.append(c.name)
        rep = [[hrep]]

        currentCell = self.down
        while currentCell is not self:
            rep[0].append(currentCell.representation())
            currentCell = currentCell.down
        
        return rep


class IncidenceMatrix(object):
    def __init__(self, names):
        self.h = ColumnObject(None, None, None, None, "root")
        self.h.left = self.h.right = self.h.up = self.h.down = self.h

        currentColumnObject = self.h
        self.columnObjectOfName = dict()
        self.columnObjectOfName["root"] = self.h

        self.indexOfPiecePlacement = dict()
        for n in names:
            self.indexOfPiecePlacement[n] = 0
            self.insertColumnObject(currentColumnObject, self.h, n)
            currentColumnObject = currentColumnObject.right
            self.columnObjectOfName[n] = currentColumnObject

        self.rows = 0

    def representation(self):
        currentColumnObject = self.h

        rep = currentColumnObject.representation()
        currentColumnObject = currentColumnObject.right

        while currentColumnObject.name is not "root":
            rep += currentColumnObject.representation()
            currentColumnObject = currentColumnObject.right
            
        return rep

    def rowRepresentation(self):
        rowRep = ""
        currentColumnObject = self.h.right
        while currentColumnObject.name is not "root" and not is_number(currentColumnObject.name):
            head_elt = currentColumnObject.down
            while head_elt is not currentColumnObject:
                row = [ head_elt.name ]
                current_elt = head_elt.right
                while current_elt is not head_elt:
                    row.append(current_elt.listHeader.name)
                    current_elt = current_elt.right
                rowRep += str(row) + "\n"
                #rowRep.append(row)
                head_elt = head_elt.down
            currentColumnObject = currentColumnObject.right
        return rowRep

    """ insert a column header object into the circular linked list that contains the "root" node """
    def insertColumnObject(self, left, right, name):
        newCO = ColumnObject(left, right, None, None, name)
        newCO.up = newCO.down = newCO
        left.right = newCO
        right.left = newCO
        return newCO

    def appendRow(self, tileName, placement):
        """ 
        a placement is a list of coordinates that indicates which squares the piece named `tileName` covers.
        This function appends a row to the incidence matrix. A row consists of
        - one IncidenceCell in the column corresponding to tileName
        - one IncidenceCell in each column corresponding to a coordinate in `placement`.
        These must be assembled into a circularly linked list, and each cell must be inserted into the 
        circular linked list of its corresponding column.
        """
        pentoHeader = self.columnObjectOfName[tileName]
        # create pentoCell
        pentoCell = IncidenceCell(None, None, pentoHeader.up, pentoHeader, pentoHeader,
                tileName+"["+str(self.indexOfPiecePlacement[tileName])+"]")
        pentoHeader.up.down = pentoCell
        pentoHeader.up = pentoCell
        pentoHeader.size = pentoHeader.size + 1
        self.indexOfPiecePlacement[tileName] += 1

        # create placementCells
        left = pentoCell
        for placeName in placement:
            placeHeader = self.columnObjectOfName[placeName]
            placementCell = IncidenceCell(left, None, placeHeader.up,
                    placeHeader, placeHeader, tileName+placeName)
            placeHeader.up.down = placementCell
            placeHeader.up = placementCell
            placeHeader.size = placeHeader.size + 1
            left.right = placementCell
            left = placementCell

        left.right = pentoCell
        pentoCell.left = left

        self.rows = self.rows + 1
        #return self

    def coverColumn(self, c):
        """ implement and document the algorithm in Knuth's paper. """
        # cover head c vertically
        c.left.right = c.right
        c.right.left = c.left

        # go through all rows in which c had a cell
        rowhead = c.down
        while rowhead is not c:
            cell = rowhead.right
            while cell is not rowhead:
                # cover the cells horizontally in these rows
                cell.up.down = cell.down
                cell.down.up = cell.up
                cell.listHeader.size -= 1
                cell = cell.right
            self.rows -= 1
            rowhead = rowhead.down
        #return self

    def uncoverColumn(self, c):
        """ implement and document the algorithm in Knuth's paper. """
        # uncover head c vertically
        c.left.right = c
        c.right.left = c

        # go through all rows in which c had a cell
        rowhead = c.up
        while rowhead is not c:
            cell = rowhead.right
            while cell is not rowhead:
                # uncover the cells horizontally in these rows
                cell.up.down = cell
                cell.down.up = cell
                cell.listHeader.size += 1
                cell = cell.right
            self.rows += 1
            rowhead = rowhead.up
        #return self

