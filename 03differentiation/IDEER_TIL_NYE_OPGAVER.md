# 📚 Idéer til nye opgavetyper for 03differentiation/

## 📌 **Formål**
Denne fil indeholder idéer til nye opgavetyper, der supplerer de eksisterende opgaver i `03differentiation/`.
Idéerne er baseret på analyser af eksisterende opgaver og identificerede mangler.

---

## 📂 **01differentiatesimpleexpressions/**
### 🔍 **Eksterne analyser**
- Grundlæggende differentiering (potensfunktioner, trigonometriske funktioner, eksponentialfunktioner, logaritmer) er dækket.
- **Mangler**: Opgaver med **inverse funktioner** (arcsin, arccos, arctan).

### ✨ **Nye opgavetyper**
1. **Differentiering af inverse trigonometriske funktioner**
   - Opgaver, der involverer differentiering af `arcsin(x)`, `arccos(x)`, `arctan(x)`.
   - Eksempel: Bestem `d/dx [arctan(3x^2 + 1)]`.

2. **Differentiering af sammensatte inverse funktioner**
   - Eksempel: Bestem `d/dx [arcsin(ln(x))]`.

---

## 📂 **02chainrule/**
### 🔍 **Eksterne analyser**
- Kædereglen er grundligt dækket.
- **Mangler**: Opgaver med **multiple sammensætninger** (f.eks. `f(g(h(x)))`).

### ✨ **Nye opgavetyper**
1. **Multiple sammensætninger**
   - Opgaver, der kræver gentagen anvendelse af kædereglen.
   - Eksempel: Bestem `d/dx [e^(sin(cos(x)))]`.

2. **Kædereglen i applikationer**
   - Opgaver, der bruger kædereglen til at modellere sammensatte funktioner i virkelige situationer.

---

## 📂 **03productrule/**
### 🔍 **Eksterne analyser**
- Produktreglen er dækket med almindelige funktioner.
- **Mangler**: Opgaver med **produkter af flere end to funktioner** (f.eks. `f(x)g(x)h(x)`).

### ✨ **Nye opgavetyper**
1. **Produkter af flere funktioner**
   - Opgaver, der involverer differentiering af produkter af 3 eller flere funktioner.
   - Eksempel: Bestem `d/dx [x^2 * sin(x) * e^x]`.

2. **Produktreglen + kædereglen**
   - Opgaver, der kombinerer produktreglen og kædereglen.
   - Eksempel: Bestem `d/dx [x * e^(x^2 + 1)]`.

---

## 📂 **04differentiatecompoundexpressions/**
### 🔍 **Eksterne analyser**
- Sammensatte funktioner med inverse trigonometriske funktioner er dækket.
- **Fejl fundet**: Nogle svar var forkerte (rettet i 2026-06-08).
- **Mangler**: Opgaver med **hyperbolske funktioner** (sinh, cosh, tanh).

### ✨ **Nye opgavetyper**
1. **Differentiering af hyperbolske funktioner**
   - Opgaver, der involverer `sinh(x)`, `cosh(x)`, `tanh(x)`.
   - Eksempel: Bestem `d/dx [sinh(2x^3 + 1)]`.

2. **Inverse hyperbolske funktioner**
   - Opgaver, der involverer `arsinh(x)`, `arcosh(x)`, `artanh(x)`.

3. **Sammensatte funktioner med rødder**
   - Eksempel: Bestem `d/dx [sqrt(sin(x^2 + 1))]`.

---

## 📂 **05linearisation/**
### 🔍 **Eksterne analyser**
- Linearisering er grundigt dækket med mange praktiske eksempler.
- **Mangler**: Opgaver med **Taylor-udviklinger af højere orden** (udover linearisering).

### ✨ **Nye opgavetyper**
1. **Taylor-udviklinger af højere orden**
   - Opgaver, der kræver udvikling af funktioner til 2. eller 3. orden.
   - Eksempel: Udvikl `f(x) = cos(x)` til 4. orden omkring `x = π/4`.

2. **Fejlvurdering i linearisering**
   - Opgaver, der involverer estimering af fejl i lineariserede approximationer.

---

## 📂 **06taylorpolynomials/**
### 🔍 **Eksterne analyser**
- Taylor-polynomier er grundigt dækket.
- **Mangler**: Opgaver med **Maclaurin-rækker** (Taylor-rækker omkring x=0).

### ✨ **Nye opgavetyper**
1. **Maclaurin-rækker**
   - Opgaver, der kræver udvikling af Maclaurin-rækker for standardfunktioner.
   - Eksempel: Udvikl Maclaurin-rækken for `f(x) = e^x` op til 5. orden.

2. **Konvergens af Taylor-rækker**
   - Opgaver, der undersøger konvergens af Taylor-rækker for forskellige funktioner.

---

## 📂 **07lhopital/**
### 🔍 **Eksterne analyser**
- L'Hopitals regel er grundigt dækket.
- **Mangler**: Opgaver med **ubestemte udtryk som ∞ - ∞, 0^0, 1^∞, ∞^0**.

### ✨ **Nye opgavetyper**
1. **Ubestemte udtryk**
   - Opgaver, der involverer ubestemte udtryk som `∞ - ∞`, `0^0`, `1^∞`.
   - Eksempel: Bestem `lim_{x->0+} x^x`.

2. **L'Hopitals regel for sekventer**
   - Opgaver, der kræver anvendelse af L'Hopitals regel på sekventer.

---

## 📂 **12partialderivatives/** og **13partialderivatives2/**
### 🔍 **Eksterne analyser**
- Partielle afledte er grundigt dækket.
- **Fejl fundet**: Syntaksfejl i `13partialderivatives2.tex` (rettet i 2026-06-08).
- **Mangler**: Opgaver med **hessisk matrix**, ** kritiske punkter**, og **optimering**.

### ✨ **Nye opgavetyper**
1. **Hessisk matrix**
   - Opgaver, der involverer beregning af den hessiske matrix for funktioner af flere variable.

2. **Klassifikation af kritiske punkter**
   - Opgaver, der kræver klassifikation af kritiske punkter (lokale/globale minima/maxima, saddelpunkter).

3. **Optimering med bibetingelser**
   - Opgaver, der involverer optimering med bibetingelser (Lagrange-multiplikatorer).

---

## 🔄 **Opdateringslog**
- **2026-06-08**: Oprettet fil med initial idéer for alle undermapper i `03differentiation/`.
