import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
search_density = 20

if __name__ == "__main__":
	i = 0
	vals = []
	for h in np.linspace(0,2,search_density):
		for x in np.linspace(0,2,search_density):
			for t in np.linspace(0,2,search_density):
				for w in np.linspace(0,2,search_density):
					print(i,'/',search_density**4)
					eq1 = ((1/3)*t*h**3+(w*t**3)/3+h**2*w*t+(t*(h-x)**3)/3+x**2*(h-x)*t)*2
					eq2 = ((107+(.101/(2*h*t+2*w*t+2*(h-x)*t))*96*2-214)*1/8)*96*1.5/60000
					val = abs(eq1-eq2)
					if val > 999999999:
						vals.append([h,x,t,w,9999999])
					else:
						vals.append([h,x,t,w,val])
					i+=1
	#print(vals)
	df = pd.DataFrame(vals, columns=['h', 'x', 't', 'w', 'epsilon'])
	print(df.sort_values(by='epsilon', ascending=True,axis=0)[:20])
	#print(df.head())
	#sns.pairplot(df)
	plt.show()
