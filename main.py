import sudoku  # Solving class
from imageProcess import ImageProcesser
import cv2
"""-----------------------------------------------------------
 Mandatory Specifications
 1-) Install tenserflow to open trained model.
 2-) Install opencv library
 """

img_path = ("image_folder/sudoku15.png")
sol_path = ("image_folder/bos.jpg")
image_processor = ImageProcesser()
resized_sol_paper = image_processor.preProcessor(img_path, sol_path)
sudoku_object = sudoku.Solver()
sudoku_object.show(image_processor.list_sudo)
index_list = sudoku_object.puzzleIndexer(image_processor.list_sudo)
solution = sudoku_object.solve(image_processor.list_sudo)
sudoku_object.show(solution)
cv2.imshow("Solution", image_processor.solution_processer(
solution, index_list, resized_sol_paper))
cv2.waitKey(0)
