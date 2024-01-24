# Getting to know the langchain API

## Step 1: Retrieval Augmented Generation for documentation website

GOAL: Parse the information on the multigrid method from the website https://julianroth.org/documentation/multigrid/basics.html and answer some questions with OpenAI's LLMs (or other open-source models).

### Results

Question: `What is the idea behind the multigrid method?`

Answer:   `The idea behind the multigrid method is to use a sequence of grids, starting from a coarse grid and refining it, to solve a linear equation system derived from a discrete weak form of a PDE. The method uses iterative solvers, such as \(\omega\)-Jacobi and Gauss-Seidel, on each grid level to achieve optimal cost complexity. The finest grid is used to assemble the system matrix and the weak form of the PDE is discretized using linear finite elements on each grid level.`

--------------------------------

Question: `Where do the linear systems come from?`

Answer:   `Linear systems come from the discretization of the weak form of a PDE using the Finite Element Method. The linear equation system is obtained by assembling the system matrix and the right-hand side vector. The system matrix is constructed using the bilinear form evaluated at the basis functions, while the right-hand side vector is computed using the linear form evaluated at the basis functions.`

---------------------------------

Question: `How can I change between coarse and fine meshes?`

Answer:   `To change between coarse and fine meshes, you need to refine the triangles of the grid. This can be done by bisecting all of the edges of a triangle and creating new triangles from the resulting nodes. By repeating this process, you can create a sequence of refined meshes.`

---------------------------------

Question: `How can I get the system matrix on the coarse mesh when I already have the system matrix on the fine mesh?`

Answer:   `To get the system matrix on the coarse mesh, you can use the refined system matrix on the fine mesh and perform a process called restriction. Restriction involves mapping the values from the fine mesh to the corresponding locations on the coarse mesh. This can be done by summing the values of the fine mesh elements that belong to each coarse mesh element.`

---------------------------------

Question: `How can I mathematically express this grid transfer?`

Answer:   `The grid transfer can be mathematically expressed using the restriction matrix \(I^{l-1}_l\) and the prolongation matrix \(I^{l}_{l-1}\). The restriction matrix maps the basis functions from level \(l\) to level \(l-1\), while the prolongation matrix maps the basis functions from level \(l-1\) to level \(l\). These matrices are dependent on the finite elements and grid refinement and have sparse entries.`

---------------------------------

Question: `What is the formula for the matrix A_{l-1}?`

Answer:   `The formula for the matrix \(A_{l-1}\) is \(A_{l-1} = I^{l}_{l-1} A_l I^{l-1}_l\).`

---------------------------------

## Step 2: Retrieval Augmented Generation for PDF document

GOAL: Parse the information on BPX and HB multielevel preconditioners from the PDF https://raw.githubusercontent.com/mathmerizing/MultigridPython/master/BPX%26HB%20Ausarbeitung.pdf and answer some questions with OpenAI's LLMs (or other open-source models).

### Results

Question: `What does HB stand for?`

Answer:   `HB stands for Hierarchical Basis.`

--------------------------------

Question: `What does BPX stand for?`

Answer:   `BPX stands for Bramble/Pasciak/Xu.`

--------------------------------

Question: `What is multigrid?`

Answer:   `Multigrid is a method used in the mechanical analysis of heterogeneous solids and for solving linear systems. It involves using a hierarchy of grids, with each grid representing a different level of detail. The method aims to solve the linear system efficiently by using a good preconditioner to reduce the number of iteration steps needed.`

--------------------------------