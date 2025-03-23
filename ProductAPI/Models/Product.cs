using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace ProductAPI.Models
{
    public class Product
    {
        [Key]
        [Column("id")]
        public int Id { get; set; }
        
        [Required]
        [StringLength(100)]
        [Column("name")]
        public string Name { get; set; } = string.Empty;
        
        [StringLength(500)]
        [Column("description")]
        public string? Description { get; set; }
        
        [Required]
        [Range(0.01, double.MaxValue)]
        [Column("price")]
        public decimal Price { get; set; }
        
        [Required]
        [Column("stock_quantity")]
        public int StockQuantity { get; set; }
        
        [Column("created_date")]
        public DateTime CreatedDate { get; set; } = DateTime.UtcNow;
        
        [Column("modified_date")]
        public DateTime? ModifiedDate { get; set; }
    }
} 