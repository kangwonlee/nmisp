# 클리브 몰러 교수님을 기리며<br>In Memoriam: Cleve Moler (1939–2026)

클리브 배리 몰러(Cleve Barry Moler, 1939–2026) 교수님께서 2026년 5월 20일, 향년 86세로 별세하셨습니다. 수학자이자 전산학자로서, 미시간 대학교·스탠퍼드 대학교·뉴멕시코 대학교에서 약 20년간 학생들을 지도하셨습니다.<br>
Professor Cleve Barry Moler (1939–2026) passed away on May 20, 2026, at the age of 86. A mathematician and computer scientist, he taught for some twenty years at the University of Michigan, Stanford University, and the University of New Mexico.

## 수치 해석 SW 공헌<br>What he built

선형대수(linear algebra)와 고유값(eigenvalue) 계산을 위한 포트란(Fortran) 라이브러리인 LINPACK과 EISPACK을 공저하셨습니다. 학생들이 포트란 코드를 직접 작성하지 않고도 이러한 강력한 라이브러리를 쓸 수 있도록, MATLAB("Matrix Laboratory")을 만드셨습니다. 그 후 1984년, 스탠퍼드 시절 당시 대학원생이었던 잭 리틀(Jack Little)과 함께 MathWorks를 공동 창업하셔서 세상에 내놓으셨습니다.<br>
He was a co-author of LINPACK and EISPACK — the Fortran libraries for linear algebra and eigenvalue computation. So that his students could use them without writing Fortran themselves, he created MATLAB ("Matrix Laboratory"); and in 1984 he co-founded MathWorks with Jack Little to bring it to the world.

## 교육자로서의 길<br>The teacher

「Numerical Computing with MATLAB」을 비롯한 저술과 오랜 칼럼 "Cleve's Corner"를 통해, 평생 동안 수치 계산(numerical computing)을 *이해할 수 있게* 만드시고자 노력하셨습니다. 미국 공학한림원(NAE, National Academy of Engineering) 회원이셨으며, 최근에는 미국 과학한림원(NAS, National Academy of Sciences) 회원으로도 선출되셨습니다.<br>
Through writings such as *Numerical Computing with MATLAB* and his long-running column *Cleve's Corner*, he devoted his life to teaching numerical computing in a way people could *understand*. He was a member of the National Academy of Engineering, and was recently elected to the National Academy of Sciences.

## 이 저장소와의 인연<br>Why this matters here

이 저장소(NMISP)의 기반이 된 NumPy·SciPy 의 `numpy.linalg`나 `scipy.linalg` 에서 실제로 실행되는 LAPACK은 바로 몰러 교수님의 LINPACK·EISPACK을 계승한 코드입니다. "알고리즘은 그저 실행되는 데 그치지 않고 이해되어야 한다"는 믿음이 NMISP를 통해서도 이어질 수 있기 바랍니다.<br>
This repository (NMISP) stands on the path he cleared. When we call `numpy.linalg` or `scipy.linalg` in NumPy/SciPy, the LAPACK running underneath is the direct descendant of Moler's LINPACK and EISPACK. His conviction — that an algorithm should be *understood*, not merely run — is the very spirit NMISP tries to carry forward.

## 개인적인 기억<br>A personal recollection

제가 대학원에서 공부하던 1990년대 초, 그분의 알고리즘 가운데 하나인 EISPACK의 `RGG`를 처음 만났습니다. 실수 일반화 고유치 문제(generalized eigenvalue problem) A x = λ B x 의 고유값과 고유벡터를 구해 주는 루틴이었습니다. 그 능력에 매료되면서도, 빽빽한 포트란(Fortran) 코드 앞에서는 적잖이 겸손해지곤 했습니다. 훗날에야 RGG가 몰러 교수님께서 1973년 G. W. 스튜어트(G. W. Stewart) 교수님과 함께 고안하신 QZ 알고리즘을 담고 있음을 알게 되었습니다. 미처 깨닫지 못한 채, 저는 이미 그분의 연구와 만나고 있었던 셈입니다.<br>
In my own graduate years, in the early 1990s, I first encountered one of his algorithms: EISPACK's `RGG`, which finds the eigenvalues and eigenvectors of the real generalized eigenproblem, A x = λ B x. I was captivated by what it could do — and humbled by the density of its Fortran code. Only later did I learn that `RGG` carries the QZ algorithm that Moler devised with G. W. Stewart in 1973. Without realizing it, I had already met his work.

## 헌사<br>Dedication

깊은 존경과 감사를 담아, 이 강의 자료를 그분의 영전에 바칩니다.<br>
With deep respect and gratitude, this course is dedicated to his memory.

---

### 더 읽을거리<br>Further reading

- [Cleve Moler — Wikipedia](https://en.wikipedia.org/wiki/Cleve_Moler)
- [Cleve Moler, founder — MathWorks](https://www.mathworks.com/company/aboutus/founders/clevemoler.html)
