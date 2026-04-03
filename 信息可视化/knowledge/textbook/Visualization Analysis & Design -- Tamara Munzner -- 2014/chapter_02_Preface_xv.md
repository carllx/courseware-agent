# Preface xv

Why a New Book? xv

Existing Books . xvi

Audience xvii

Who’s Who xviii

Structure: What’s in This Book xviii

What’s Not in This Book xx

Acknowledgments . xx

# 1 What’s Vis, and Why Do It? 1

1.1 The Big Picture . 1   
1.2 Why Have a Human in the Loop? 2   
1.3 Why Have a Computer in the Loop? . 4   
1.4 Why Use an External Representation? 6   
1.5 Why Depend on Vision? . 6   
1.6 Why Show the Data in Detail? 7   
1.7 Why Use Interactivity? . . 9   
1.8 Why Is the Vis Idiom Design Space Huge? 10   
1.9 Why Focus on Tasks? 11   
1.10 Why Focus on Effectiveness? . 11   
1.11 Why Are Most Designs Ineffective? . 12   
1.12 Why Is Validation Difficult? . 14   
1.13 Why Are There Resource Limitations? . 14   
1.14 Why Analyze? . 16   
1.15 Further Reading 18

# 2 What: Data Abstraction 20

2.1 The Big Picture . . 21   
2.2 Why Do Data Semantics and Types Matter? 21   
2.3 Data Types 23   
2.4 Dataset Types . . . 24

2.4.1 Tables 25   
2.4.2 Networks and Trees . . 26   
2.4.2.1 Trees . . 27

2.4.3 Fields 27

2.4.3.1 Spatial Fields 28   
2.4.3.2 Grid Types 29

2.4.4 Geometry 29   
2.4.5 Other Combinations . . 30   
2.4.6 Dataset Availability 31

2.5 Attribute Types . . 31

2.5.1 Categorical 32   
2.5.2 Ordered: Ordinal and Quantitative . . 32

2.5.2.1 Sequential versus Diverging . . 33   
2.5.2.2 Cyclic 33

2.5.3 Hierarchical Attributes 33

2.6 Semantics . 34

2.6.1 Key versus Value Semantics 34

2.6.1.1 Flat Tables 34   
2.6.1.2 Multidimensional Tables 36   
2.6.1.3 Fields 37   
2.6.1.4 Scalar Fields 37   
2.6.1.5 Vector Fields 37   
2.6.1.6 Tensor Fields 38   
2.6.1.7 Field Semantics 38

2.6.2 Temporal Semantics . 38

2.6.2.1 Time-Varying Data . . 39

2.7 Further Reading 40

3 Why: Task Abstraction 42

3.1 The Big Picture . 43   
3.2 Why Analyze Tasks Abstractly? 43   
3.3 Who: Designer or User 44   
3.4 Actions . . 45

3.4.1 Analyze . 45

3.4.1.1 Discover . 47   
3.4.1.2 Present 47   
3.4.1.3 Enjoy 48

3.4.2 Produce 49

3.4.2.1 Annotate 49   
3.4.2.2 Record . 49  
3.4.2.3 Derive 50

3.4.3 Search . 53

3.4.3.1 Lookup 53  
3.4.3.2 Locate 53   
3.4.3.3 Browse . 53   
3.4.3.4 Explore 54

3.4.4 Query 54

3.4.4.1 Identify 54   
3.4.4.2 Compare . . 55   
3.4.4.3 Summarize 55

3.5 Targets . . 55   
3.6 How: A Preview 57

3.7 Analyzing and Deriving: Examples . . 59

3.7.1 Comparing Two Idioms . . 59   
3.7.2 Deriving One Attribute 60   
3.7.3 Deriving Many New Attributes . . 62

3.8 Further Reading 64

4 Analysis: Four Levels for Validation 66

4.1 The Big Picture . 67   
4.2 Why Validate? . 67

4.3 Four Levels of Design 67

4.3.1 Domain Situation 69   
4.3.2 Task and Data Abstraction . 70   
4.3.3 Visual Encoding and Interaction Idiom . 71   
4.3.4 Algorithm 72

4.4 Angles of Attack 73

4.5 Threats to Validity 74   
4.6 Validation Approaches . 75

4.6.1 Domain Validation . 77   
4.6.2 Abstraction Validation 78   
4.6.3 Idiom Validation 78   
4.6.4 Algorithm Validation . 80   
4.6.5 Mismatches . 81

4.7 Validation Examples . . 81

4.7.1 Genealogical Graphs 81   
4.7.2 MatrixExplorer . . 83   
4.7.3 Flow Maps 85   
4.7.4 LiveRAC 87   
4.7.5 LinLog . . 89   
4.7.6 Sizing the Horizon 90

4.8 Further Reading 91

5 Marks and Channels 94

5.1 The Big Picture . . 95   
5.2 Why Marks and Channels? 95   
5.3 Defining Marks and Channels 95

5.3.1 Channel Types . . 99   
5.3.2 Mark Types . . 99

5.4 Using Marks and Channels . 99

5.4.1 Expressiveness and Effectiveness 100   
5.4.2 Channel Rankings . . 101

5.5 Channel Effectiveness . 103

5.5.1 Accuracy 103   
5.5.2 Discriminability 106   
5.5.3 Separability . . 106   
5.5.4 Popout . . . 109   
5.5.5 Grouping 111

5.6 Relative versus Absolute Judgements . 112   
5.7 Further Reading 114

6 Rules of Thumb 116

6.1 The Big Picture . . 117   
6.2 Why and When to Follow Rules of Thumb? . 117   
6.3 No Unjustified 3D 117

6.3.1 The Power of the Plane 118   
6.3.2 The Disparity of Depth 118   
6.3.3 Occlusion Hides Information . . 120   
6.3.4 Perspective Distortion Dangers 121   
6.3.5 Other Depth Cues . 123   
6.3.6 Tilted Text Isn’t Legibile . . 124   
6.3.7 Benefits of 3D: Shape Perception 124   
6.3.8 Justification and Alternatives 125

Example: Cluster–Calendar Time-Series Vis 125

Example: Layer-Oriented Time-Series Vis 128

6.3.9 Empirical Evidence 129

6.4 No Unjustified 2D 131   
6.5 Eyes Beat Memory . . 131

6.5.1 Memory and Attention 132   
6.5.2 Animation versus Side-by-Side Views . . 132   
6.5.3 Change Blindness 133

6.6 Resolution over Immersion 134   
6.7 Overview First, Zoom and Filter, Details on Demand 135   
6.8 Responsiveness Is Required 137

6.8.1 Visual Feedback 138   
6.8.2 Latency and Interaction Design . 138   
6.8.3 Interactivity Costs 140

6.9 Get It Right in Black and White 140   
6.10 Function First, Form Next 140   
6.11 Further Reading 141

# 7 Arrange Tables 144

7.1 The Big Picture . . 145   
7.2 Why Arrange? . . 145   
7.3 Arrange by Keys and Values 145   
7.4 Express: Quantitative Values . . 146

Example: Scatterplots 146

7.5 Separate, Order, and Align: Categorical Regions . . . 149

7.5.1 List Alignment: One Key . 149

Example: Bar Charts 150   
Example: Stacked Bar Charts 151   
Example: Streamgraphs 153   
Example: Dot and Line Charts 155

7.5.2 Matrix Alignment: Two Keys . . 157

Example: Cluster Heatmaps 158   
Example: Scatterplot Matrix . 160

7.5.3 Volumetric Grid: Three Keys . . 161   
7.5.4 Recursive Subdivision: Multiple Keys . . . 161

7.6 Spatial Axis Orientation . 162

7.6.1 Rectilinear Layouts 162   
7.6.2 Parallel Layouts 162

Example: Parallel Coordinates 162

7.6.3 Radial Layouts . 166

Example: Radial Bar Charts 167   
Example: Pie Charts 168

7.7 Spatial Layout Density . . 171

7.7.1 Dense 172   
Example: Dense Software Overviews 172

7.7.2 Space-Filling . . 174   
7.8 Further Reading . . . 175

# 8 Arrange Spatial Data 178

8.1 The Big Picture . 179   
8.2 Why Use Given? 179   
8.3 Geometry 180

8.3.1 Geographic Data . 180   
Example: Choropleth Maps 181

8.3.2 Other Derived Geometry 182

8.4 Scalar Fields: One Value 182

8.4.1 Isocontours . 183

Example: Topographic Terrain Maps 183   
Example: Flexible Isosurfaces 185

8.4.2 Direct Volume Rendering . . 186

Example: Multidimensional Transfer Functions 187

8.5 Vector Fields: Multiple Values 189

8.5.1 Flow Glyphs 191   
8.5.2 Geometric Flow 191   
Example: Similarity-Clustered Streamlines 192   
8.5.3 Texture Flow 193   
8.5.4 Feature Flow 193

8.6 Tensor Fields: Many Values . . 194

Example: Ellipsoid Tensor Glyphs 194

8.7 Further Reading . . . 197

9 Arrange Networks and Trees 200

9.1 The Big Picture . . 201   
9.2 Connection: Link Marks . 201

Example: Force-Directed Placement 204   
Example: sfdp 207

9.3 Matrix Views 208

Example: Adjacency Matrix View 208

9.4 Costs and Benefits: Connection versus Matrix . 209   
9.5 Containment: Hierarchy Marks 213

Example: Treemaps 213   
Example: GrouseFlocks 215

9.6 Further Reading 216

10 Map Color and Other Channels 218

10.1 The Big Picture . 219   
10.2 Color Theory 219

10.2.1 Color Vision 219   
10.2.2 Color Spaces 220   
10.2.3 Luminance, Saturation, and Hue . 223   
10.2.4 Transparency . . 225

10.3 Colormaps . . 225

10.3.1 Categorical Colormaps 226   
10.3.2 Ordered Colormaps . 229   
10.3.3 Bivariate Colormaps . . 234   
10.3.4 Colorblind-Safe Colormap Design . . 235

10.4 Other Channels . 236

10.4.1 Size Channels 236   
10.4.2 Angle Channel 237   
10.4.3 Curvature Channel 238   
10.4.4 Shape Channel . 238   
10.4.5 Motion Channels . . 238   
10.4.6 Texture and Stippling . . 239

10.5 Further Reading 240

# 11 Manipulate View 242

11.1 The Big Picture . 243   
11.2 Why Change? . 244   
11.3 Change View over Time 244

Example: LineUp 246

Example: Animated Transitions 248

11.4 Select Elements . 249

11.4.1 Selection Design Choices . 250   
11.4.2 Highlighting 251

Example: Context-Preserving Visual Links 253

11.4.3 Selection Outcomes 254

11.5 Navigate: Changing Viewpoint . . 254

11.5.1 Geometric Zooming . 255   
11.5.2 Semantic Zooming . . 255   
11.5.3 Constrained Navigation . 256

11.6 Navigate: Reducing Attributes . 258

11.6.1 Slice 258   
Example: HyperSlice 259   
11.6.2 Cut . 260   
11.6.3 Project . . 261

11.7 Further Reading 261

# 12 Facet into Multiple Views 264

12.1 The Big Picture . 265   
12.2 Why Facet? 265

12.3 Juxtapose and Coordinate Views 267

12.3.1 Share Encoding: Same/Different 267   
Example: Exploratory Data Visualizer (EDV) 268

Share Data: All, Subset, None . . 269   
Example: Bird’s-Eye Maps 270   
Example: Multiform Overview–Detail Microarrays 271   
Example: Cerebral 274

12.3.3 Share Navigation: Synchronize 276   
12.3.4 Combinations 276

Example: Improvise 277   
12.3.5 Juxtapose Views . 278

12.4 Partition into Views 279

12.4.1 Regions, Glyphs, and Views 279   
12.4.2 List Alignments 281

12.4.3 Matrix Alignments . 282   
Example: Trellis 282   
12.4.4 Recursive Subdivision . 285

12.5 Superimpose Layers . . 288

12.5.1 Visually Distinguishable Layers . . 289   
12.5.2 Static Layers . . 289

Example: Cartographic Layering 289   
Example: Superimposed Line Charts . 290   
Example: Hierarchical Edge Bundles . 292

12.5.3 Dynamic Layers . 294

12.6 Further Reading . . 295

13 Reduce Items and Attributes 298

13.1 The Big Picture . . 299   
13.2 Why Reduce? 299   
13.3 Filter 300

13.3.1 Item Filtering . 301   
Example: FilmFinder 301   
13.3.2 Attribute Filtering 303   
Example: DOSFA 304

13.4 Aggregate 305

13.4.1 Item Aggregation . 305

Example: Histograms 306   
Example: Continuous Scatterplots 307   
Example: Boxplot Charts . 308   
Example: SolarPlot 310   
Example: Hierarchical Parallel Coordinates 311

13.4.2 Spatial Aggregation 313

Example: Geographically Weighted Boxplots 313

13.4.3 Attribute Aggregation: Dimensionality Reduction . 315

13.4.3.1 Why and When to Use DR? . 316   
Example: Dimensionality Reduction for Document Collections . 316   
13.4.3.2 How to Show DR Data? . 319

13.5 Further Reading 320

14 Embed: Focus+Context 322

14.1 The Big Picture . 323   
14.2 Why Embed? 323   
14.3 Elide 324   
Example: DOITrees Revisited 325   
14.4 Superimpose 326   
Example: Toolglass and Magic Lenses 326   
14.5 Distort 327   
Example: 3D Perspective . . 327   
Example: Fisheye Lens 328   
Example: Hyperbolic Geometry 329

Example: Stretch and Squish Navigation 331

Example: Nonlinear Magnification Fields 333

14.6 Costs and Benefits: Distortion 334   
14.7 Further Reading 337

15 Analysis Case Studies 340

15.1 The Big Picture . 341   
15.2 Why Analyze Case Studies? . 341   
15.3 Graph-Theoretic Scagnostics . . 342   
15.4 VisDB 347   
15.5 Hierarchical Clustering Explorer . . 351   
15.6 PivotGraph 355   
15.7 InterRing 358   
15.8 Constellation 360   
15.9 Further Reading 366

Figure Credits 369

Bibliography 375

Idiom and System Examples Index 397

Concept Index 399

![](images/1c296ab0b2e9fd74f89da5e3a59c7b115bc0038eae981dd648799142390a01b9.jpg)

#

