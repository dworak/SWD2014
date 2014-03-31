from scipy.spatial.distance import euclidean, cityblock, mahalanobis
from numpy.linalg import inv
from numpy import cov

class Metryka():
    
    def metrykaEuklidesowa(self, array1, array2):
        """
        Computes the Euclidean distance between two n-vectors ``u`` and ``v``,
        which is defined as
    
        .. math::
    
           {||u-v||}_2
    
        Parameters
        ----------
        u : ndarray
            An :math:`n`-dimensional vector.
        v : ndarray
            An :math:`n`-dimensional vector.
    
        Returns
        -------
        d : double
            The Euclidean distance between vectors ``u`` and ``v``.
        """
        # od = sqrt [ (xa-xb)^2 + (ya-yb)^2]
        return euclidean(array1, array2)
    
    def metrykaManhattan(self, array1, array2):
        """
        Computes the Manhattan distance between two n-vectors u and v,
        which is defined as
    
        .. math::
    
           \\sum_i {\\left| u_i - v_i \\right|}.
    
        Parameters
        ----------
        u : ndarray
            An :math:`n`-dimensional vector.
        v : ndarray
            An :math:`n`-dimensional vector.
    
        Returns
        -------
        d : double
            The City Block distance between vectors ``u`` and ``v``.
    
        """
        # od = abs(xa-xb) + abs(ya-yb)
        return cityblock(array1,array2)
    
    def metrykaMahalanobisa(self,array1,array2):
        
        macierzKowariancji = inv(cov(array1,array2))
        """
        Computes the Mahalanobis distance between two n-vectors ``u`` and ``v``,
        which is defined as
    
        .. math::
    
           \sqrt{ (u-v) V^{-1} (u-v)^T }
    
        where ``V`` is the covariance matrix.  Note that the argument ``VI``
        is the inverse of ``V``.
    
        Parameters
        ----------
        u : ndarray
            An :math:`n`-dimensional vector.
        v : ndarray
            An :math:`n`-dimensional vector.
        VI : ndarray
            The inverse of the covariance matrix.
    
        Returns
        -------
        d : double
            The Mahalanobis distance between vectors ``u`` and ``v``.
        """
        return mahalanobis(array1, array2, macierzKowariancji)
    
    