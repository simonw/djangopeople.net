/* 0.9.7 on Wed Mar 25 11:29:32 2009 */

#define PY_SSIZE_T_CLEAN
#include "Python.h"
#include "structmember.h"
#ifndef PY_LONG_LONG
  #define PY_LONG_LONG LONG_LONG
#endif
#if PY_VERSION_HEX < 0x02050000
  typedef int Py_ssize_t;
  #define PY_SSIZE_T_MAX INT_MAX
  #define PY_SSIZE_T_MIN INT_MIN
  #define PyInt_FromSsize_t(z) PyInt_FromLong(z)
  #define PyInt_AsSsize_t(o)	PyInt_AsLong(o)
#endif
#ifndef WIN32
  #ifndef __stdcall
    #define __stdcall
  #endif
  #ifndef __cdecl
    #define __cdecl
  #endif
#endif
#ifdef __cplusplus
#define __PYX_EXTERN_C extern "C"
#else
#define __PYX_EXTERN_C extern
#endif
#include <math.h>


typedef struct {PyObject **p; char *s;} __Pyx_InternTabEntry; /*proto*/
typedef struct {PyObject **p; char *s; long n;} __Pyx_StringTabEntry; /*proto*/

static PyObject *__pyx_m;
static PyObject *__pyx_b;
static int __pyx_lineno;
static char *__pyx_filename;
static char **__pyx_f;

static int __Pyx_ArgTypeTest(PyObject *obj, PyTypeObject *type, int none_allowed, char *name); /*proto*/

static void __Pyx_Raise(PyObject *type, PyObject *value, PyObject *tb); /*proto*/

static PyObject *__Pyx_UnpackItem(PyObject *); /*proto*/
static int __Pyx_EndUnpack(PyObject *); /*proto*/

static PyObject *__Pyx_GetName(PyObject *dict, PyObject *name); /*proto*/

static int __Pyx_InternStrings(__Pyx_InternTabEntry *t); /*proto*/

static int __Pyx_InitStrings(__Pyx_StringTabEntry *t); /*proto*/

static void __Pyx_AddTraceback(char *funcname); /*proto*/

/* Declarations from closestpair */



/* Implementation of closestpair */

static PyObject *__pyx_f_11closestpair_distance(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds); /*proto*/
static char __pyx_doc_11closestpair_distance[] = "Pythagorean distance";
static PyObject *__pyx_f_11closestpair_distance(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds) {
  float __pyx_v_x1;
  float __pyx_v_y1;
  float __pyx_v_x2;
  float __pyx_v_y2;
  PyObject *__pyx_r;
  PyObject *__pyx_1 = 0;
  static char *__pyx_argnames[] = {"x1","y1","x2","y2",0};
  if (!PyArg_ParseTupleAndKeywords(__pyx_args, __pyx_kwds, "ffff", __pyx_argnames, &__pyx_v_x1, &__pyx_v_y1, &__pyx_v_x2, &__pyx_v_y2)) return 0;
  __pyx_1 = PyFloat_FromDouble(pow((pow((__pyx_v_x1 - __pyx_v_x2), 2) + pow((__pyx_v_y1 - __pyx_v_y2), 2)), 0.5)); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 4; goto __pyx_L1;}
  __pyx_r = __pyx_1;
  __pyx_1 = 0;
  goto __pyx_L0;

  __pyx_r = Py_None; Py_INCREF(Py_None);
  goto __pyx_L0;
  __pyx_L1:;
  Py_XDECREF(__pyx_1);
  __Pyx_AddTraceback("closestpair.distance");
  __pyx_r = 0;
  __pyx_L0:;
  return __pyx_r;
}

static PyObject *__pyx_n_distance;
static PyObject *__pyx_n_closest_pair;
static PyObject *__pyx_n_min;
static PyObject *__pyx_n_append;
static PyObject *__pyx_n_sort;

static PyObject *__pyx_k1p;

static char __pyx_k1[] = "Single or empty points set";

static PyObject *__pyx_f_11closestpair_closest_pair(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds); /*proto*/
static char __pyx_doc_11closestpair_closest_pair[] = "\n    Returns the closest pair of points as (distance, (x, y, data), (x2, y2, data2)).\n    \n    @param points: A list of triples (x, y, data)\n    ";
static PyObject *__pyx_f_11closestpair_closest_pair(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds) {
  PyListObject *__pyx_v_points = 0;
  float __pyx_v_min_d;
  PyObject *__pyx_v_min_p1;
  PyObject *__pyx_v_min_p2;
  PyObject *__pyx_v_i;
  PyObject *__pyx_v_point;
  PyObject *__pyx_v_point2;
  PyObject *__pyx_v_d;
  PyObject *__pyx_v_split;
  PyObject *__pyx_v_d1;
  PyObject *__pyx_v_p11;
  PyObject *__pyx_v_p12;
  PyObject *__pyx_v_d2;
  PyObject *__pyx_v_p21;
  PyObject *__pyx_v_p22;
  PyObject *__pyx_v_points_in_strip;
  PyObject *__pyx_v_split_at;
  PyObject *__pyx_v_max_i;
  PyObject *__pyx_v_sd;
  PyObject *__pyx_r;
  Py_ssize_t __pyx_1;
  int __pyx_2;
  PyObject *__pyx_3 = 0;
  PyObject *__pyx_4 = 0;
  PyObject *__pyx_5 = 0;
  PyObject *__pyx_6 = 0;
  PyObject *__pyx_7 = 0;
  PyObject *__pyx_8 = 0;
  PyObject *__pyx_9 = 0;
  PyObject *__pyx_10 = 0;
  float __pyx_11;
  int __pyx_12;
  Py_ssize_t __pyx_13;
  static char *__pyx_argnames[] = {"points",0};
  if (!PyArg_ParseTupleAndKeywords(__pyx_args, __pyx_kwds, "O", __pyx_argnames, &__pyx_v_points)) return 0;
  Py_INCREF(__pyx_v_points);
  __pyx_v_min_p1 = Py_None; Py_INCREF(Py_None);
  __pyx_v_min_p2 = Py_None; Py_INCREF(Py_None);
  __pyx_v_i = Py_None; Py_INCREF(Py_None);
  __pyx_v_point = Py_None; Py_INCREF(Py_None);
  __pyx_v_point2 = Py_None; Py_INCREF(Py_None);
  __pyx_v_d = Py_None; Py_INCREF(Py_None);
  __pyx_v_split = Py_None; Py_INCREF(Py_None);
  __pyx_v_d1 = Py_None; Py_INCREF(Py_None);
  __pyx_v_p11 = Py_None; Py_INCREF(Py_None);
  __pyx_v_p12 = Py_None; Py_INCREF(Py_None);
  __pyx_v_d2 = Py_None; Py_INCREF(Py_None);
  __pyx_v_p21 = Py_None; Py_INCREF(Py_None);
  __pyx_v_p22 = Py_None; Py_INCREF(Py_None);
  __pyx_v_points_in_strip = Py_None; Py_INCREF(Py_None);
  __pyx_v_split_at = Py_None; Py_INCREF(Py_None);
  __pyx_v_max_i = Py_None; Py_INCREF(Py_None);
  __pyx_v_sd = Py_None; Py_INCREF(Py_None);
  if (!__Pyx_ArgTypeTest(((PyObject *)__pyx_v_points), (&PyList_Type), 1, "points")) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 6; goto __pyx_L1;}

  /* "/home/andrew/Programs/cluster/clusterer/closestpair.pyx":15 */
  __pyx_1 = PyObject_Length(((PyObject *)__pyx_v_points)); if (__pyx_1 == -1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 15; goto __pyx_L1;}
  __pyx_2 = (__pyx_1 < 2);
  if (__pyx_2) {
    __pyx_3 = PyTuple_New(1); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 16; goto __pyx_L1;}
    Py_INCREF(__pyx_k1p);
    PyTuple_SET_ITEM(__pyx_3, 0, __pyx_k1p);
    __pyx_4 = PyObject_CallObject(PyExc_ValueError, __pyx_3); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 16; goto __pyx_L1;}
    Py_DECREF(__pyx_3); __pyx_3 = 0;
    __Pyx_Raise(__pyx_4, 0, 0);
    Py_DECREF(__pyx_4); __pyx_4 = 0;
    {__pyx_filename = __pyx_f[0]; __pyx_lineno = 16; goto __pyx_L1;}
    goto __pyx_L2;
  }
  __pyx_1 = PyObject_Length(((PyObject *)__pyx_v_points)); if (__pyx_1 == -1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 17; goto __pyx_L1;}
  __pyx_2 = 2 <= __pyx_1;
  if (__pyx_2) {
    __pyx_2 = __pyx_1 <= 6;
  }
  if (__pyx_2) {

    /* "/home/andrew/Programs/cluster/clusterer/closestpair.pyx":18 */
    __pyx_v_min_d = 0;

    /* "/home/andrew/Programs/cluster/clusterer/closestpair.pyx":19 */
    Py_INCREF(Py_None);
    Py_DECREF(__pyx_v_min_p1);
    __pyx_v_min_p1 = Py_None;

    /* "/home/andrew/Programs/cluster/clusterer/closestpair.pyx":20 */
    Py_INCREF(Py_None);
    Py_DECREF(__pyx_v_min_p2);
    __pyx_v_min_p2 = Py_None;

    /* "/home/andrew/Programs/cluster/clusterer/closestpair.pyx":21 */
    __pyx_3 = PyTuple_New(1); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 21; goto __pyx_L1;}
    Py_INCREF(((PyObject *)__pyx_v_points));
    PyTuple_SET_ITEM(__pyx_3, 0, ((PyObject *)__pyx_v_points));
    __pyx_4 = PyObject_CallObject(((PyObject *)(&PyEnum_Type)), __pyx_3); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 21; goto __pyx_L1;}
    Py_DECREF(__pyx_3); __pyx_3 = 0;
    __pyx_3 = PyObject_GetIter(__pyx_4); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 21; goto __pyx_L1;}
    Py_DECREF(__pyx_4); __pyx_4 = 0;
    for (;;) {
      __pyx_4 = PyIter_Next(__pyx_3);
      if (!__pyx_4) {
        if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 21; goto __pyx_L1;}
        break;
      }
      __pyx_5 = PyObject_GetIter(__pyx_4); if (!__pyx_5) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 21; goto __pyx_L1;}
      Py_DECREF(__pyx_4); __pyx_4 = 0;
      __pyx_4 = __Pyx_UnpackItem(__pyx_5); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 21; goto __pyx_L1;}
      Py_DECREF(__pyx_v_i);
      __pyx_v_i = __pyx_4;
      __pyx_4 = 0;
      __pyx_4 = __Pyx_UnpackItem(__pyx_5); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 21; goto __pyx_L1;}
      Py_DECREF(__pyx_v_point);
      __pyx_v_point = __pyx_4;
      __pyx_4 = 0;
      if (__Pyx_EndUnpack(__pyx_5) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 21; goto __pyx_L1;}
      Py_DECREF(__pyx_5); __pyx_5 = 0;
      __pyx_4 = PyInt_FromLong(1); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 22; goto __pyx_L1;}
      __pyx_5 = PyNumber_Add(__pyx_v_i, __pyx_4); if (!__pyx_5) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 22; goto __pyx_L1;}
      Py_DECREF(__pyx_4); __pyx_4 = 0;
      __pyx_1 = PyInt_AsSsize_t(__pyx_5); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 22; goto __pyx_L1;}
      Py_DECREF(__pyx_5); __pyx_5 = 0;
      __pyx_4 = PySequence_GetSlice(((PyObject *)__pyx_v_points), __pyx_1, PY_SSIZE_T_MAX); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 22; goto __pyx_L1;}
      __pyx_5 = PyObject_GetIter(__pyx_4); if (!__pyx_5) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 22; goto __pyx_L1;}
      Py_DECREF(__pyx_4); __pyx_4 = 0;
      for (;;) {
        __pyx_4 = PyIter_Next(__pyx_5);
        if (!__pyx_4) {
          if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 22; goto __pyx_L1;}
          break;
        }
        Py_DECREF(__pyx_v_point2);
        __pyx_v_point2 = __pyx_4;
        __pyx_4 = 0;

        /* "/home/andrew/Programs/cluster/clusterer/closestpair.pyx":23 */
        __pyx_4 = __Pyx_GetName(__pyx_m, __pyx_n_distance); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 23; goto __pyx_L1;}
        __pyx_6 = PySequence_GetItem(__pyx_v_point, 0); if (!__pyx_6) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 23; goto __pyx_L1;}
        __pyx_7 = PySequence_GetItem(__pyx_v_point, 1); if (!__pyx_7) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 23; goto __pyx_L1;}
        __pyx_8 = PySequence_GetItem(__pyx_v_point2, 0); if (!__pyx_8) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 23; goto __pyx_L1;}
        __pyx_9 = PySequence_GetItem(__pyx_v_point2, 1); if (!__pyx_9) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 23; goto __pyx_L1;}
        __pyx_10 = PyTuple_New(4); if (!__pyx_10) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 23; goto __pyx_L1;}
        PyTuple_SET_ITEM(__pyx_10, 0, __pyx_6);
        PyTuple_SET_ITEM(__pyx_10, 1, __pyx_7);
        PyTuple_SET_ITEM(__pyx_10, 2, __pyx_8);
        PyTuple_SET_ITEM(__pyx_10, 3, __pyx_9);
        __pyx_6 = 0;
        __pyx_7 = 0;
        __pyx_8 = 0;
        __pyx_9 = 0;
        __pyx_6 = PyObject_CallObject(__pyx_4, __pyx_10); if (!__pyx_6) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 23; goto __pyx_L1;}
        Py_DECREF(__pyx_4); __pyx_4 = 0;
        Py_DECREF(__pyx_10); __pyx_10 = 0;
        Py_DECREF(__pyx_v_d);
        __pyx_v_d = __pyx_6;
        __pyx_6 = 0;

        /* "/home/andrew/Programs/cluster/clusterer/closestpair.pyx":24 */
        __pyx_2 = (__pyx_v_min_d == 0);
        if (!__pyx_2) {
          __pyx_7 = PyFloat_FromDouble(__pyx_v_min_d); if (!__pyx_7) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 24; goto __pyx_L1;}
          if (PyObject_Cmp(__pyx_7, __pyx_v_d, &__pyx_2) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 24; goto __pyx_L1;}
          __pyx_2 = __pyx_2 > 0;
          Py_DECREF(__pyx_7); __pyx_7 = 0;
        }
        if (__pyx_2) {

          /* "/home/andrew/Programs/cluster/clusterer/closestpair.pyx":25 */
          __pyx_11 = PyFloat_AsDouble(__pyx_v_d); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 25; goto __pyx_L1;}
          __pyx_v_min_d = __pyx_11;

          /* "/home/andrew/Programs/cluster/clusterer/closestpair.pyx":26 */
          Py_INCREF(__pyx_v_point);
          Py_DECREF(__pyx_v_min_p1);
          __pyx_v_min_p1 = __pyx_v_point;

          /* "/home/andrew/Programs/cluster/clusterer/closestpair.pyx":27 */
          Py_INCREF(__pyx_v_point2);
          Py_DECREF(__pyx_v_min_p2);
          __pyx_v_min_p2 = __pyx_v_point2;
          goto __pyx_L7;
        }
        __pyx_L7:;
      }
      Py_DECREF(__pyx_5); __pyx_5 = 0;
    }
    Py_DECREF(__pyx_3); __pyx_3 = 0;

    /* "/home/andrew/Programs/cluster/clusterer/closestpair.pyx":28 */
    __pyx_8 = PyFloat_FromDouble(__pyx_v_min_d); if (!__pyx_8) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 28; goto __pyx_L1;}
    __pyx_9 = PyTuple_New(3); if (!__pyx_9) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 28; goto __pyx_L1;}
    PyTuple_SET_ITEM(__pyx_9, 0, __pyx_8);
    Py_INCREF(__pyx_v_min_p1);
    PyTuple_SET_ITEM(__pyx_9, 1, __pyx_v_min_p1);
    Py_INCREF(__pyx_v_min_p2);
    PyTuple_SET_ITEM(__pyx_9, 2, __pyx_v_min_p2);
    __pyx_8 = 0;
    __pyx_r = __pyx_9;
    __pyx_9 = 0;
    goto __pyx_L0;
    goto __pyx_L2;
  }
  /*else*/ {

    /* "/home/andrew/Programs/cluster/clusterer/closestpair.pyx":30 */
    __pyx_12 = PyList_Sort(((PyObject *)__pyx_v_points)); if (__pyx_12 == -1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 30; goto __pyx_L1;}

    /* "/home/andrew/Programs/cluster/clusterer/closestpair.pyx":32 */
    __pyx_1 = PyObject_Length(((PyObject *)__pyx_v_points)); if (__pyx_1 == -1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 32; goto __pyx_L1;}
    __pyx_4 = PyInt_FromSsize_t((__pyx_1 / 2)); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 32; goto __pyx_L1;}
    __pyx_10 = PyTuple_New(1); if (!__pyx_10) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 32; goto __pyx_L1;}
    PyTuple_SET_ITEM(__pyx_10, 0, __pyx_4);
    __pyx_4 = 0;
    __pyx_6 = PyObject_CallObject(((PyObject *)(&PyInt_Type)), __pyx_10); if (!__pyx_6) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 32; goto __pyx_L1;}
    Py_DECREF(__pyx_10); __pyx_10 = 0;
    Py_DECREF(__pyx_v_split);
    __pyx_v_split = __pyx_6;
    __pyx_6 = 0;

    /* "/home/andrew/Programs/cluster/clusterer/closestpair.pyx":33 */
    __pyx_7 = __Pyx_GetName(__pyx_m, __pyx_n_closest_pair); if (!__pyx_7) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 33; goto __pyx_L1;}
    __pyx_1 = PyInt_AsSsize_t(__pyx_v_split); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 33; goto __pyx_L1;}
    __pyx_5 = PySequence_GetSlice(((PyObject *)__pyx_v_points), 0, __pyx_1); if (!__pyx_5) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 33; goto __pyx_L1;}
    __pyx_3 = PyTuple_New(1); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 33; goto __pyx_L1;}
    PyTuple_SET_ITEM(__pyx_3, 0, __pyx_5);
    __pyx_5 = 0;
    __pyx_8 = PyObject_CallObject(__pyx_7, __pyx_3); if (!__pyx_8) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 33; goto __pyx_L1;}
    Py_DECREF(__pyx_7); __pyx_7 = 0;
    Py_DECREF(__pyx_3); __pyx_3 = 0;
    __pyx_9 = PyObject_GetIter(__pyx_8); if (!__pyx_9) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 33; goto __pyx_L1;}
    Py_DECREF(__pyx_8); __pyx_8 = 0;
    __pyx_4 = __Pyx_UnpackItem(__pyx_9); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 33; goto __pyx_L1;}
    Py_DECREF(__pyx_v_d1);
    __pyx_v_d1 = __pyx_4;
    __pyx_4 = 0;
    __pyx_10 = __Pyx_UnpackItem(__pyx_9); if (!__pyx_10) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 33; goto __pyx_L1;}
    Py_DECREF(__pyx_v_p11);
    __pyx_v_p11 = __pyx_10;
    __pyx_10 = 0;
    __pyx_6 = __Pyx_UnpackItem(__pyx_9); if (!__pyx_6) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 33; goto __pyx_L1;}
    Py_DECREF(__pyx_v_p12);
    __pyx_v_p12 = __pyx_6;
    __pyx_6 = 0;
    if (__Pyx_EndUnpack(__pyx_9) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 33; goto __pyx_L1;}
    Py_DECREF(__pyx_9); __pyx_9 = 0;

    /* "/home/andrew/Programs/cluster/clusterer/closestpair.pyx":34 */
    __pyx_5 = __Pyx_GetName(__pyx_m, __pyx_n_closest_pair); if (!__pyx_5) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 34; goto __pyx_L1;}
    __pyx_1 = PyInt_AsSsize_t(__pyx_v_split); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 34; goto __pyx_L1;}
    __pyx_7 = PySequence_GetSlice(((PyObject *)__pyx_v_points), __pyx_1, PY_SSIZE_T_MAX); if (!__pyx_7) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 34; goto __pyx_L1;}
    __pyx_3 = PyTuple_New(1); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 34; goto __pyx_L1;}
    PyTuple_SET_ITEM(__pyx_3, 0, __pyx_7);
    __pyx_7 = 0;
    __pyx_8 = PyObject_CallObject(__pyx_5, __pyx_3); if (!__pyx_8) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 34; goto __pyx_L1;}
    Py_DECREF(__pyx_5); __pyx_5 = 0;
    Py_DECREF(__pyx_3); __pyx_3 = 0;
    __pyx_4 = PyObject_GetIter(__pyx_8); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 34; goto __pyx_L1;}
    Py_DECREF(__pyx_8); __pyx_8 = 0;
    __pyx_10 = __Pyx_UnpackItem(__pyx_4); if (!__pyx_10) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 34; goto __pyx_L1;}
    Py_DECREF(__pyx_v_d2);
    __pyx_v_d2 = __pyx_10;
    __pyx_10 = 0;
    __pyx_6 = __Pyx_UnpackItem(__pyx_4); if (!__pyx_6) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 34; goto __pyx_L1;}
    Py_DECREF(__pyx_v_p21);
    __pyx_v_p21 = __pyx_6;
    __pyx_6 = 0;
    __pyx_9 = __Pyx_UnpackItem(__pyx_4); if (!__pyx_9) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 34; goto __pyx_L1;}
    Py_DECREF(__pyx_v_p22);
    __pyx_v_p22 = __pyx_9;
    __pyx_9 = 0;
    if (__Pyx_EndUnpack(__pyx_4) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 34; goto __pyx_L1;}
    Py_DECREF(__pyx_4); __pyx_4 = 0;

    /* "/home/andrew/Programs/cluster/clusterer/closestpair.pyx":35 */
    __pyx_7 = __Pyx_GetName(__pyx_b, __pyx_n_min); if (!__pyx_7) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 35; goto __pyx_L1;}
    __pyx_5 = PyTuple_New(2); if (!__pyx_5) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 35; goto __pyx_L1;}
    Py_INCREF(__pyx_v_d1);
    PyTuple_SET_ITEM(__pyx_5, 0, __pyx_v_d1);
    Py_INCREF(__pyx_v_d2);
    PyTuple_SET_ITEM(__pyx_5, 1, __pyx_v_d2);
    __pyx_3 = PyObject_CallObject(__pyx_7, __pyx_5); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 35; goto __pyx_L1;}
    Py_DECREF(__pyx_7); __pyx_7 = 0;
    Py_DECREF(__pyx_5); __pyx_5 = 0;
    Py_DECREF(__pyx_v_d);
    __pyx_v_d = __pyx_3;
    __pyx_3 = 0;

    /* "/home/andrew/Programs/cluster/clusterer/closestpair.pyx":37 */
    __pyx_8 = PyList_New(0); if (!__pyx_8) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 37; goto __pyx_L1;}
    Py_DECREF(__pyx_v_points_in_strip);
    __pyx_v_points_in_strip = __pyx_8;
    __pyx_8 = 0;

    /* "/home/andrew/Programs/cluster/clusterer/closestpair.pyx":38 */
    __pyx_10 = PyInt_FromLong(1); if (!__pyx_10) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 38; goto __pyx_L1;}
    __pyx_6 = PyNumber_Subtract(__pyx_v_split, __pyx_10); if (!__pyx_6) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 38; goto __pyx_L1;}
    Py_DECREF(__pyx_10); __pyx_10 = 0;
    __pyx_9 = PyObject_GetItem(((PyObject *)__pyx_v_points), __pyx_6); if (!__pyx_9) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 38; goto __pyx_L1;}
    Py_DECREF(__pyx_6); __pyx_6 = 0;
    __pyx_4 = PySequence_GetItem(__pyx_9, 0); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 38; goto __pyx_L1;}
    Py_DECREF(__pyx_9); __pyx_9 = 0;
    __pyx_7 = PyObject_GetItem(((PyObject *)__pyx_v_points), __pyx_v_split); if (!__pyx_7) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 38; goto __pyx_L1;}
    __pyx_5 = PySequence_GetItem(__pyx_7, 0); if (!__pyx_5) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 38; goto __pyx_L1;}
    Py_DECREF(__pyx_7); __pyx_7 = 0;
    __pyx_3 = PyNumber_Add(__pyx_4, __pyx_5); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 38; goto __pyx_L1;}
    Py_DECREF(__pyx_4); __pyx_4 = 0;
    Py_DECREF(__pyx_5); __pyx_5 = 0;
    __pyx_8 = PyFloat_FromDouble(2.0); if (!__pyx_8) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 38; goto __pyx_L1;}
    __pyx_10 = PyNumber_Divide(__pyx_3, __pyx_8); if (!__pyx_10) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 38; goto __pyx_L1;}
    Py_DECREF(__pyx_3); __pyx_3 = 0;
    Py_DECREF(__pyx_8); __pyx_8 = 0;
    Py_DECREF(__pyx_v_split_at);
    __pyx_v_split_at = __pyx_10;
    __pyx_10 = 0;

    /* "/home/andrew/Programs/cluster/clusterer/closestpair.pyx":39 */
    __pyx_6 = PyObject_GetIter(((PyObject *)__pyx_v_points)); if (!__pyx_6) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 39; goto __pyx_L1;}
    for (;;) {
      __pyx_9 = PyIter_Next(__pyx_6);
      if (!__pyx_9) {
        if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 39; goto __pyx_L1;}
        break;
      }
      Py_DECREF(__pyx_v_point);
      __pyx_v_point = __pyx_9;
      __pyx_9 = 0;

      /* "/home/andrew/Programs/cluster/clusterer/closestpair.pyx":40 */
      __pyx_7 = PySequence_GetItem(__pyx_v_point, 0); if (!__pyx_7) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 40; goto __pyx_L1;}
      __pyx_4 = PyNumber_Subtract(__pyx_v_split_at, __pyx_v_d); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 40; goto __pyx_L1;}
      if (PyObject_Cmp(__pyx_7, __pyx_4, &__pyx_2) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 40; goto __pyx_L1;}
      __pyx_2 = __pyx_2 < 0;
      Py_DECREF(__pyx_7); __pyx_7 = 0;
      Py_DECREF(__pyx_4); __pyx_4 = 0;
      if (__pyx_2) {
        goto __pyx_L8;
        goto __pyx_L10;
      }
      __pyx_5 = PySequence_GetItem(__pyx_v_point, 0); if (!__pyx_5) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 42; goto __pyx_L1;}
      __pyx_3 = PyNumber_Add(__pyx_v_split_at, __pyx_v_d); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 42; goto __pyx_L1;}
      if (PyObject_Cmp(__pyx_5, __pyx_3, &__pyx_2) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 42; goto __pyx_L1;}
      __pyx_2 = __pyx_2 > 0;
      Py_DECREF(__pyx_5); __pyx_5 = 0;
      Py_DECREF(__pyx_3); __pyx_3 = 0;
      if (__pyx_2) {
        goto __pyx_L9;
        goto __pyx_L10;
      }
      __pyx_L10:;

      /* "/home/andrew/Programs/cluster/clusterer/closestpair.pyx":44 */
      __pyx_8 = PyObject_GetAttr(__pyx_v_points_in_strip, __pyx_n_append); if (!__pyx_8) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 44; goto __pyx_L1;}
      __pyx_10 = PySequence_GetItem(__pyx_v_point, 1); if (!__pyx_10) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 44; goto __pyx_L1;}
      __pyx_9 = PySequence_GetItem(__pyx_v_point, 0); if (!__pyx_9) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 44; goto __pyx_L1;}
      __pyx_7 = PySequence_GetItem(__pyx_v_point, 2); if (!__pyx_7) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 44; goto __pyx_L1;}
      __pyx_4 = PyTuple_New(3); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 44; goto __pyx_L1;}
      PyTuple_SET_ITEM(__pyx_4, 0, __pyx_10);
      PyTuple_SET_ITEM(__pyx_4, 1, __pyx_9);
      PyTuple_SET_ITEM(__pyx_4, 2, __pyx_7);
      __pyx_10 = 0;
      __pyx_9 = 0;
      __pyx_7 = 0;
      __pyx_5 = PyTuple_New(1); if (!__pyx_5) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 44; goto __pyx_L1;}
      PyTuple_SET_ITEM(__pyx_5, 0, __pyx_4);
      __pyx_4 = 0;
      __pyx_3 = PyObject_CallObject(__pyx_8, __pyx_5); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 44; goto __pyx_L1;}
      Py_DECREF(__pyx_8); __pyx_8 = 0;
      Py_DECREF(__pyx_5); __pyx_5 = 0;
      Py_DECREF(__pyx_3); __pyx_3 = 0;
      __pyx_L8:;
    }
    __pyx_L9:;
    Py_DECREF(__pyx_6); __pyx_6 = 0;

    /* "/home/andrew/Programs/cluster/clusterer/closestpair.pyx":46 */
    __pyx_10 = PyObject_GetAttr(__pyx_v_points_in_strip, __pyx_n_sort); if (!__pyx_10) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 46; goto __pyx_L1;}
    __pyx_9 = PyObject_CallObject(__pyx_10, 0); if (!__pyx_9) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 46; goto __pyx_L1;}
    Py_DECREF(__pyx_10); __pyx_10 = 0;
    Py_DECREF(__pyx_9); __pyx_9 = 0;

    /* "/home/andrew/Programs/cluster/clusterer/closestpair.pyx":48 */
    __pyx_v_min_d = 0;

    /* "/home/andrew/Programs/cluster/clusterer/closestpair.pyx":49 */
    Py_INCREF(Py_None);
    Py_DECREF(__pyx_v_min_p1);
    __pyx_v_min_p1 = Py_None;

    /* "/home/andrew/Programs/cluster/clusterer/closestpair.pyx":50 */
    Py_INCREF(Py_None);
    Py_DECREF(__pyx_v_min_p2);
    __pyx_v_min_p2 = Py_None;

    /* "/home/andrew/Programs/cluster/clusterer/closestpair.pyx":51 */
    __pyx_1 = PyObject_Length(__pyx_v_points_in_strip); if (__pyx_1 == -1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 51; goto __pyx_L1;}
    __pyx_7 = PyInt_FromSsize_t(__pyx_1); if (!__pyx_7) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 51; goto __pyx_L1;}
    Py_DECREF(__pyx_v_max_i);
    __pyx_v_max_i = __pyx_7;
    __pyx_7 = 0;

    /* "/home/andrew/Programs/cluster/clusterer/closestpair.pyx":52 */
    __pyx_4 = PyTuple_New(1); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 52; goto __pyx_L1;}
    Py_INCREF(__pyx_v_points_in_strip);
    PyTuple_SET_ITEM(__pyx_4, 0, __pyx_v_points_in_strip);
    __pyx_8 = PyObject_CallObject(((PyObject *)(&PyEnum_Type)), __pyx_4); if (!__pyx_8) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 52; goto __pyx_L1;}
    Py_DECREF(__pyx_4); __pyx_4 = 0;
    __pyx_5 = PyObject_GetIter(__pyx_8); if (!__pyx_5) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 52; goto __pyx_L1;}
    Py_DECREF(__pyx_8); __pyx_8 = 0;
    for (;;) {
      __pyx_3 = PyIter_Next(__pyx_5);
      if (!__pyx_3) {
        if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 52; goto __pyx_L1;}
        break;
      }
      __pyx_6 = PyObject_GetIter(__pyx_3); if (!__pyx_6) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 52; goto __pyx_L1;}
      Py_DECREF(__pyx_3); __pyx_3 = 0;
      __pyx_10 = __Pyx_UnpackItem(__pyx_6); if (!__pyx_10) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 52; goto __pyx_L1;}
      Py_DECREF(__pyx_v_i);
      __pyx_v_i = __pyx_10;
      __pyx_10 = 0;
      __pyx_9 = __Pyx_UnpackItem(__pyx_6); if (!__pyx_9) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 52; goto __pyx_L1;}
      Py_DECREF(__pyx_v_point);
      __pyx_v_point = __pyx_9;
      __pyx_9 = 0;
      if (__Pyx_EndUnpack(__pyx_6) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 52; goto __pyx_L1;}
      Py_DECREF(__pyx_6); __pyx_6 = 0;
      __pyx_7 = PyInt_FromLong(1); if (!__pyx_7) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 53; goto __pyx_L1;}
      __pyx_4 = PyNumber_Add(__pyx_v_i, __pyx_7); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 53; goto __pyx_L1;}
      Py_DECREF(__pyx_7); __pyx_7 = 0;
      __pyx_1 = PyInt_AsSsize_t(__pyx_4); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 53; goto __pyx_L1;}
      Py_DECREF(__pyx_4); __pyx_4 = 0;
      __pyx_8 = __Pyx_GetName(__pyx_b, __pyx_n_min); if (!__pyx_8) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 53; goto __pyx_L1;}
      __pyx_3 = PyInt_FromLong(7); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 53; goto __pyx_L1;}
      __pyx_10 = PyNumber_Add(__pyx_v_i, __pyx_3); if (!__pyx_10) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 53; goto __pyx_L1;}
      Py_DECREF(__pyx_3); __pyx_3 = 0;
      __pyx_9 = PyTuple_New(2); if (!__pyx_9) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 53; goto __pyx_L1;}
      Py_INCREF(__pyx_v_max_i);
      PyTuple_SET_ITEM(__pyx_9, 0, __pyx_v_max_i);
      PyTuple_SET_ITEM(__pyx_9, 1, __pyx_10);
      __pyx_10 = 0;
      __pyx_6 = PyObject_CallObject(__pyx_8, __pyx_9); if (!__pyx_6) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 53; goto __pyx_L1;}
      Py_DECREF(__pyx_8); __pyx_8 = 0;
      Py_DECREF(__pyx_9); __pyx_9 = 0;
      __pyx_13 = PyInt_AsSsize_t(__pyx_6); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 53; goto __pyx_L1;}
      Py_DECREF(__pyx_6); __pyx_6 = 0;
      __pyx_7 = PySequence_GetSlice(__pyx_v_points_in_strip, __pyx_1, __pyx_13); if (!__pyx_7) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 53; goto __pyx_L1;}
      __pyx_4 = PyObject_GetIter(__pyx_7); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 53; goto __pyx_L1;}
      Py_DECREF(__pyx_7); __pyx_7 = 0;
      for (;;) {
        __pyx_3 = PyIter_Next(__pyx_4);
        if (!__pyx_3) {
          if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 53; goto __pyx_L1;}
          break;
        }
        Py_DECREF(__pyx_v_point2);
        __pyx_v_point2 = __pyx_3;
        __pyx_3 = 0;

        /* "/home/andrew/Programs/cluster/clusterer/closestpair.pyx":54 */
        __pyx_10 = __Pyx_GetName(__pyx_m, __pyx_n_distance); if (!__pyx_10) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 54; goto __pyx_L1;}
        __pyx_8 = PySequence_GetItem(__pyx_v_point, 0); if (!__pyx_8) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 54; goto __pyx_L1;}
        __pyx_9 = PySequence_GetItem(__pyx_v_point, 1); if (!__pyx_9) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 54; goto __pyx_L1;}
        __pyx_6 = PySequence_GetItem(__pyx_v_point2, 0); if (!__pyx_6) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 54; goto __pyx_L1;}
        __pyx_7 = PySequence_GetItem(__pyx_v_point2, 1); if (!__pyx_7) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 54; goto __pyx_L1;}
        __pyx_3 = PyTuple_New(4); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 54; goto __pyx_L1;}
        PyTuple_SET_ITEM(__pyx_3, 0, __pyx_8);
        PyTuple_SET_ITEM(__pyx_3, 1, __pyx_9);
        PyTuple_SET_ITEM(__pyx_3, 2, __pyx_6);
        PyTuple_SET_ITEM(__pyx_3, 3, __pyx_7);
        __pyx_8 = 0;
        __pyx_9 = 0;
        __pyx_6 = 0;
        __pyx_7 = 0;
        __pyx_8 = PyObject_CallObject(__pyx_10, __pyx_3); if (!__pyx_8) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 54; goto __pyx_L1;}
        Py_DECREF(__pyx_10); __pyx_10 = 0;
        Py_DECREF(__pyx_3); __pyx_3 = 0;
        Py_DECREF(__pyx_v_sd);
        __pyx_v_sd = __pyx_8;
        __pyx_8 = 0;

        /* "/home/andrew/Programs/cluster/clusterer/closestpair.pyx":55 */
        __pyx_2 = (__pyx_v_min_d == 0);
        if (!__pyx_2) {
          __pyx_9 = PyFloat_FromDouble(__pyx_v_min_d); if (!__pyx_9) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 55; goto __pyx_L1;}
          if (PyObject_Cmp(__pyx_9, __pyx_v_sd, &__pyx_2) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 55; goto __pyx_L1;}
          __pyx_2 = __pyx_2 > 0;
          Py_DECREF(__pyx_9); __pyx_9 = 0;
        }
        if (__pyx_2) {

          /* "/home/andrew/Programs/cluster/clusterer/closestpair.pyx":56 */
          __pyx_11 = PyFloat_AsDouble(__pyx_v_sd); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 56; goto __pyx_L1;}
          __pyx_v_min_d = __pyx_11;

          /* "/home/andrew/Programs/cluster/clusterer/closestpair.pyx":57 */
          __pyx_6 = PySequence_GetItem(__pyx_v_point, 1); if (!__pyx_6) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 57; goto __pyx_L1;}
          __pyx_7 = PySequence_GetItem(__pyx_v_point, 0); if (!__pyx_7) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 57; goto __pyx_L1;}
          __pyx_10 = PySequence_GetItem(__pyx_v_point, 2); if (!__pyx_10) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 57; goto __pyx_L1;}
          __pyx_3 = PyTuple_New(3); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 57; goto __pyx_L1;}
          PyTuple_SET_ITEM(__pyx_3, 0, __pyx_6);
          PyTuple_SET_ITEM(__pyx_3, 1, __pyx_7);
          PyTuple_SET_ITEM(__pyx_3, 2, __pyx_10);
          __pyx_6 = 0;
          __pyx_7 = 0;
          __pyx_10 = 0;
          Py_DECREF(__pyx_v_min_p1);
          __pyx_v_min_p1 = __pyx_3;
          __pyx_3 = 0;

          /* "/home/andrew/Programs/cluster/clusterer/closestpair.pyx":58 */
          __pyx_8 = PySequence_GetItem(__pyx_v_point2, 1); if (!__pyx_8) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 58; goto __pyx_L1;}
          __pyx_9 = PySequence_GetItem(__pyx_v_point2, 0); if (!__pyx_9) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 58; goto __pyx_L1;}
          __pyx_6 = PySequence_GetItem(__pyx_v_point2, 2); if (!__pyx_6) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 58; goto __pyx_L1;}
          __pyx_7 = PyTuple_New(3); if (!__pyx_7) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 58; goto __pyx_L1;}
          PyTuple_SET_ITEM(__pyx_7, 0, __pyx_8);
          PyTuple_SET_ITEM(__pyx_7, 1, __pyx_9);
          PyTuple_SET_ITEM(__pyx_7, 2, __pyx_6);
          __pyx_8 = 0;
          __pyx_9 = 0;
          __pyx_6 = 0;
          Py_DECREF(__pyx_v_min_p2);
          __pyx_v_min_p2 = __pyx_7;
          __pyx_7 = 0;
          goto __pyx_L15;
        }
        __pyx_L15:;
      }
      Py_DECREF(__pyx_4); __pyx_4 = 0;
    }
    Py_DECREF(__pyx_5); __pyx_5 = 0;

    /* "/home/andrew/Programs/cluster/clusterer/closestpair.pyx":59 */
    __pyx_2 = (__pyx_v_min_d != 0);
    if (__pyx_2) {
      __pyx_10 = PyFloat_FromDouble(__pyx_v_min_d); if (!__pyx_10) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 59; goto __pyx_L1;}
      if (PyObject_Cmp(__pyx_10, __pyx_v_d, &__pyx_2) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 59; goto __pyx_L1;}
      __pyx_2 = __pyx_2 < 0;
      Py_DECREF(__pyx_10); __pyx_10 = 0;
    }
    if (__pyx_2) {
      __pyx_3 = PyFloat_FromDouble(__pyx_v_min_d); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 60; goto __pyx_L1;}
      __pyx_8 = PyTuple_New(3); if (!__pyx_8) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 60; goto __pyx_L1;}
      PyTuple_SET_ITEM(__pyx_8, 0, __pyx_3);
      Py_INCREF(__pyx_v_min_p1);
      PyTuple_SET_ITEM(__pyx_8, 1, __pyx_v_min_p1);
      Py_INCREF(__pyx_v_min_p2);
      PyTuple_SET_ITEM(__pyx_8, 2, __pyx_v_min_p2);
      __pyx_3 = 0;
      __pyx_r = __pyx_8;
      __pyx_8 = 0;
      goto __pyx_L0;
      goto __pyx_L16;
    }
    if (PyObject_Cmp(__pyx_v_d1, __pyx_v_d2, &__pyx_2) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 61; goto __pyx_L1;}
    __pyx_2 = __pyx_2 < 0;
    if (__pyx_2) {
      __pyx_9 = PyTuple_New(3); if (!__pyx_9) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 62; goto __pyx_L1;}
      Py_INCREF(__pyx_v_d1);
      PyTuple_SET_ITEM(__pyx_9, 0, __pyx_v_d1);
      Py_INCREF(__pyx_v_p11);
      PyTuple_SET_ITEM(__pyx_9, 1, __pyx_v_p11);
      Py_INCREF(__pyx_v_p12);
      PyTuple_SET_ITEM(__pyx_9, 2, __pyx_v_p12);
      __pyx_r = __pyx_9;
      __pyx_9 = 0;
      goto __pyx_L0;
      goto __pyx_L16;
    }
    /*else*/ {
      __pyx_6 = PyTuple_New(3); if (!__pyx_6) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 64; goto __pyx_L1;}
      Py_INCREF(__pyx_v_d2);
      PyTuple_SET_ITEM(__pyx_6, 0, __pyx_v_d2);
      Py_INCREF(__pyx_v_p21);
      PyTuple_SET_ITEM(__pyx_6, 1, __pyx_v_p21);
      Py_INCREF(__pyx_v_p22);
      PyTuple_SET_ITEM(__pyx_6, 2, __pyx_v_p22);
      __pyx_r = __pyx_6;
      __pyx_6 = 0;
      goto __pyx_L0;
    }
    __pyx_L16:;
  }
  __pyx_L2:;

  __pyx_r = Py_None; Py_INCREF(Py_None);
  goto __pyx_L0;
  __pyx_L1:;
  Py_XDECREF(__pyx_3);
  Py_XDECREF(__pyx_4);
  Py_XDECREF(__pyx_5);
  Py_XDECREF(__pyx_6);
  Py_XDECREF(__pyx_7);
  Py_XDECREF(__pyx_8);
  Py_XDECREF(__pyx_9);
  Py_XDECREF(__pyx_10);
  __Pyx_AddTraceback("closestpair.closest_pair");
  __pyx_r = 0;
  __pyx_L0:;
  Py_DECREF(__pyx_v_min_p1);
  Py_DECREF(__pyx_v_min_p2);
  Py_DECREF(__pyx_v_i);
  Py_DECREF(__pyx_v_point);
  Py_DECREF(__pyx_v_point2);
  Py_DECREF(__pyx_v_d);
  Py_DECREF(__pyx_v_split);
  Py_DECREF(__pyx_v_d1);
  Py_DECREF(__pyx_v_p11);
  Py_DECREF(__pyx_v_p12);
  Py_DECREF(__pyx_v_d2);
  Py_DECREF(__pyx_v_p21);
  Py_DECREF(__pyx_v_p22);
  Py_DECREF(__pyx_v_points_in_strip);
  Py_DECREF(__pyx_v_split_at);
  Py_DECREF(__pyx_v_max_i);
  Py_DECREF(__pyx_v_sd);
  Py_DECREF(__pyx_v_points);
  return __pyx_r;
}

static __Pyx_InternTabEntry __pyx_intern_tab[] = {
  {&__pyx_n_append, "append"},
  {&__pyx_n_closest_pair, "closest_pair"},
  {&__pyx_n_distance, "distance"},
  {&__pyx_n_min, "min"},
  {&__pyx_n_sort, "sort"},
  {0, 0}
};

static __Pyx_StringTabEntry __pyx_string_tab[] = {
  {&__pyx_k1p, __pyx_k1, sizeof(__pyx_k1)},
  {0, 0, 0}
};

static struct PyMethodDef __pyx_methods[] = {
  {"distance", (PyCFunction)__pyx_f_11closestpair_distance, METH_VARARGS|METH_KEYWORDS, __pyx_doc_11closestpair_distance},
  {"closest_pair", (PyCFunction)__pyx_f_11closestpair_closest_pair, METH_VARARGS|METH_KEYWORDS, __pyx_doc_11closestpair_closest_pair},
  {0, 0, 0, 0}
};

static void __pyx_init_filenames(void); /*proto*/

PyMODINIT_FUNC initclosestpair(void); /*proto*/
PyMODINIT_FUNC initclosestpair(void) {
  __pyx_init_filenames();
  __pyx_m = Py_InitModule4("closestpair", __pyx_methods, 0, 0, PYTHON_API_VERSION);
  if (!__pyx_m) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 2; goto __pyx_L1;};
  Py_INCREF(__pyx_m);
  __pyx_b = PyImport_AddModule("__builtin__");
  if (!__pyx_b) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 2; goto __pyx_L1;};
  if (PyObject_SetAttrString(__pyx_m, "__builtins__", __pyx_b) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 2; goto __pyx_L1;};
  if (__Pyx_InternStrings(__pyx_intern_tab) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 2; goto __pyx_L1;};
  if (__Pyx_InitStrings(__pyx_string_tab) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 2; goto __pyx_L1;};

  /* "/home/andrew/Programs/cluster/clusterer/closestpair.pyx":6 */
  return;
  __pyx_L1:;
  __Pyx_AddTraceback("closestpair");
}

static char *__pyx_filenames[] = {
  "closestpair.pyx",
};

/* Runtime support code */

static void __pyx_init_filenames(void) {
  __pyx_f = __pyx_filenames;
}

static int __Pyx_ArgTypeTest(PyObject *obj, PyTypeObject *type, int none_allowed, char *name) {
    if (!type) {
        PyErr_Format(PyExc_SystemError, "Missing type object");
        return 0;
    }
    if ((none_allowed && obj == Py_None) || PyObject_TypeCheck(obj, type))
        return 1;
    PyErr_Format(PyExc_TypeError,
        "Argument '%s' has incorrect type (expected %s, got %s)",
        name, type->tp_name, obj->ob_type->tp_name);
    return 0;
}

static void __Pyx_Raise(PyObject *type, PyObject *value, PyObject *tb) {
    Py_XINCREF(type);
    Py_XINCREF(value);
    Py_XINCREF(tb);
    /* First, check the traceback argument, replacing None with NULL. */
    if (tb == Py_None) {
        Py_DECREF(tb);
        tb = 0;
    }
    else if (tb != NULL && !PyTraceBack_Check(tb)) {
        PyErr_SetString(PyExc_TypeError,
            "raise: arg 3 must be a traceback or None");
        goto raise_error;
    }
    /* Next, replace a missing value with None */
    if (value == NULL) {
        value = Py_None;
        Py_INCREF(value);
    }
    #if PY_VERSION_HEX < 0x02050000
    if (!PyClass_Check(type))
    #else
    if (!PyType_Check(type))
    #endif
    {
        /* Raising an instance.  The value should be a dummy. */
        if (value != Py_None) {
            PyErr_SetString(PyExc_TypeError,
                "instance exception may not have a separate value");
            goto raise_error;
        }
        /* Normalize to raise <class>, <instance> */
        Py_DECREF(value);
        value = type;
        #if PY_VERSION_HEX < 0x02050000
            if (PyInstance_Check(type)) {
                type = (PyObject*) ((PyInstanceObject*)type)->in_class;
                Py_INCREF(type);
            }
            else {
                PyErr_SetString(PyExc_TypeError,
                    "raise: exception must be an old-style class or instance");
                goto raise_error;
            }
        #else
            type = (PyObject*) type->ob_type;
            Py_INCREF(type);
            if (!PyType_IsSubtype((PyTypeObject *)type, (PyTypeObject *)PyExc_BaseException)) {
                PyErr_SetString(PyExc_TypeError,
                    "raise: exception class must be a subclass of BaseException");
                goto raise_error;
            }
        #endif
    }
    PyErr_Restore(type, value, tb);
    return;
raise_error:
    Py_XDECREF(value);
    Py_XDECREF(type);
    Py_XDECREF(tb);
    return;
}

static void __Pyx_UnpackError(void) {
    PyErr_SetString(PyExc_ValueError, "unpack sequence of wrong size");
}

static PyObject *__Pyx_UnpackItem(PyObject *iter) {
    PyObject *item;
    if (!(item = PyIter_Next(iter))) {
        if (!PyErr_Occurred())
            __Pyx_UnpackError();
    }
    return item;
}

static int __Pyx_EndUnpack(PyObject *iter) {
    PyObject *item;
    if ((item = PyIter_Next(iter))) {
        Py_DECREF(item);
        __Pyx_UnpackError();
        return -1;
    }
    else if (!PyErr_Occurred())
        return 0;
    else
        return -1;
}

static PyObject *__Pyx_GetName(PyObject *dict, PyObject *name) {
    PyObject *result;
    result = PyObject_GetAttr(dict, name);
    if (!result)
        PyErr_SetObject(PyExc_NameError, name);
    return result;
}

static int __Pyx_InternStrings(__Pyx_InternTabEntry *t) {
    while (t->p) {
        *t->p = PyString_InternFromString(t->s);
        if (!*t->p)
            return -1;
        ++t;
    }
    return 0;
}

static int __Pyx_InitStrings(__Pyx_StringTabEntry *t) {
    while (t->p) {
        *t->p = PyString_FromStringAndSize(t->s, t->n - 1);
        if (!*t->p)
            return -1;
        ++t;
    }
    return 0;
}

#include "compile.h"
#include "frameobject.h"
#include "traceback.h"

static void __Pyx_AddTraceback(char *funcname) {
    PyObject *py_srcfile = 0;
    PyObject *py_funcname = 0;
    PyObject *py_globals = 0;
    PyObject *empty_tuple = 0;
    PyObject *empty_string = 0;
    PyCodeObject *py_code = 0;
    PyFrameObject *py_frame = 0;
    
    py_srcfile = PyString_FromString(__pyx_filename);
    if (!py_srcfile) goto bad;
    py_funcname = PyString_FromString(funcname);
    if (!py_funcname) goto bad;
    py_globals = PyModule_GetDict(__pyx_m);
    if (!py_globals) goto bad;
    empty_tuple = PyTuple_New(0);
    if (!empty_tuple) goto bad;
    empty_string = PyString_FromString("");
    if (!empty_string) goto bad;
    py_code = PyCode_New(
        0,            /*int argcount,*/
        0,            /*int nlocals,*/
        0,            /*int stacksize,*/
        0,            /*int flags,*/
        empty_string, /*PyObject *code,*/
        empty_tuple,  /*PyObject *consts,*/
        empty_tuple,  /*PyObject *names,*/
        empty_tuple,  /*PyObject *varnames,*/
        empty_tuple,  /*PyObject *freevars,*/
        empty_tuple,  /*PyObject *cellvars,*/
        py_srcfile,   /*PyObject *filename,*/
        py_funcname,  /*PyObject *name,*/
        __pyx_lineno,   /*int firstlineno,*/
        empty_string  /*PyObject *lnotab*/
    );
    if (!py_code) goto bad;
    py_frame = PyFrame_New(
        PyThreadState_Get(), /*PyThreadState *tstate,*/
        py_code,             /*PyCodeObject *code,*/
        py_globals,          /*PyObject *globals,*/
        0                    /*PyObject *locals*/
    );
    if (!py_frame) goto bad;
    py_frame->f_lineno = __pyx_lineno;
    PyTraceBack_Here(py_frame);
bad:
    Py_XDECREF(py_srcfile);
    Py_XDECREF(py_funcname);
    Py_XDECREF(empty_tuple);
    Py_XDECREF(empty_string);
    Py_XDECREF(py_code);
    Py_XDECREF(py_frame);
}
