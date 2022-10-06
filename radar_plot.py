
from matplotlib import pyplot as plt
import math

def make_radar(df, artist_name):
    
    values = df.loc['mean'].values.tolist()
    categories = df.columns
    N = len(categories)
    angles = [n / float(N) * 2 * math.pi for n in range(N)]
    angles += angles[:1]
    values += values[:1]
    # Initialise the spider plot
    ax = plt.subplot(111, polar=True)
 
    # Draw one axe per variable + add labels
    plt.xticks(angles[:-1], categories, color='black', size=16)
    
    # Draw ylabels
    ax.set_rlabel_position(0)
    ax.tick_params(axis="both", which="major", pad=25)
    plt.ylim(0,1)
    ax.plot(angles, values, 'o--', linewidth=2, color='black')
    
    #Changing the padding of spider labels
    XTICKS = ax.xaxis.get_major_ticks()
    XTICKS[0].set_pad(60)
    XTICKS[1].set_pad(10)
    XTICKS[2].set_pad(10)
    XTICKS[3].set_pad(40)
    # Fill area
    ax.fill(angles, values, 'b', alpha=0.1)
    # Show the graph
    #plt.title(artist_name, size=20, pad=50)
    #plt.tight_layout()
    plt.savefig('radar_plot'+ artist_name + '.png', dpi=500)
    #plt.show()
